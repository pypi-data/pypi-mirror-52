import asyncio
from typing import (  # noqa: F401
    Any,
    Awaitable,
    List,
    Sequence,
    TypeVar,
    cast,
)

from .exceptions import (
    EventLoopMismatch,
    OperationCancelled,
)

_R = TypeVar('_R')


class CancelToken:
    def __init__(self, name: str, loop: asyncio.AbstractEventLoop = None) -> None:
        self.name = name
        self._chain: List['CancelToken'] = []
        self._triggered = asyncio.Event(loop=loop)
        self._loop = loop

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        """
        Return the `loop` that this token is bound to.
        """
        return self._loop

    def chain(self, token: 'CancelToken') -> 'CancelToken':
        """
        Return a new CancelToken chaining this and the given token.

        The new CancelToken's triggered will return True if trigger() has been
        called on either of the chained tokens, but calling trigger() on the new token
        has no effect on either of the chained tokens.
        """
        if self.loop != token._loop:
            raise EventLoopMismatch("Chained CancelToken objects must be on the same event loop")
        chain_name = ":".join([self.name, token.name])
        chain = CancelToken(chain_name, loop=self.loop)
        chain._chain.extend([self, token])
        return chain

    def trigger(self) -> None:
        """
        Trigger this cancel token and any child tokens that have been chained with it.
        """
        self._triggered.set()

    @property
    def triggered_token(self) -> 'CancelToken':
        """
        Return the token which was triggered.

        The returned token may be this token or one that it was chained with.
        """
        if self._triggered.is_set():
            return self
        for token in self._chain:
            if token.triggered:
                # Use token.triggered_token here to make the lookup recursive as self._chain may
                # contain other chains.
                return token.triggered_token
        return None

    @property
    def triggered(self) -> bool:
        """
        Return `True` or `False` whether this token has been triggered.
        """
        if self._triggered.is_set():
            return True
        return any(token.triggered for token in self._chain)

    def raise_if_triggered(self) -> None:
        """
        Raise `OperationCancelled` if this token has been triggered.
        """
        if self.triggered:
            raise OperationCancelled(
                "Cancellation requested by {} token".format(self.triggered_token))

    async def wait(self) -> None:
        """
        Coroutine which returns when this token has been triggered
        """
        if self.triggered_token is not None:
            return

        futures = [asyncio.ensure_future(self._triggered.wait(), loop=self.loop)]
        for token in self._chain:
            futures.append(asyncio.ensure_future(token.wait(), loop=self.loop))

        try:
            done, pending = await asyncio.wait(
                futures,
                return_when=asyncio.FIRST_COMPLETED,
                loop=self.loop,
            )
        except asyncio.CancelledError as err:
            # Since we use return_when=asyncio.FIRST_COMPLETED above, we can
            # be sure none of our futures will be done here, so we don't need
            # to check if any is done before cancelling.
            for future in futures:
                future.cancel()
            for future in futures:
                try:
                    await future
                except asyncio.CancelledError:
                    pass
            raise err
        else:
            for future in pending:
                future.cancel()
            for future in pending:
                try:
                    await future
                except asyncio.CancelledError:
                    pass

    async def cancellable_wait(self, *awaitables: Awaitable[_R], timeout: float = None) -> _R:
        """
        Wait for the first awaitable to complete, unless we timeout or the
        token is triggered.

        Returns the result of the first awaitable to complete.

        Raises TimeoutError if we timeout or
        `~cancel_token.exceptions.OperationCancelled` if the cancel token is
        triggered.

        All pending futures are cancelled before returning.
        """
        futures = [asyncio.ensure_future(a, loop=self.loop) for a in awaitables + (self.wait(),)]
        try:
            done, pending = await asyncio.wait(
                futures,
                timeout=timeout,
                return_when=asyncio.FIRST_COMPLETED,
                loop=self.loop,
            )
        except asyncio.CancelledError as err:
            # Since we use return_when=asyncio.FIRST_COMPLETED above, we can
            # be sure none of our futures will be done here, so we don't need
            # to check if any is done before cancelling.
            for future in futures:
                future.cancel()
            for future in futures:
                try:
                    await future
                except asyncio.CancelledError:
                    pass
            raise err
        else:
            for future in pending:
                future.cancel()
            for future in pending:
                try:
                    await future
                except asyncio.CancelledError:
                    pass

        if not done:
            raise asyncio.TimeoutError()

        if self.triggered_token is not None:
            # We've been asked to cancel so we don't care about our future, but we must
            # consume its exception or else asyncio will emit warnings.
            for task in done:
                task.result()
            raise OperationCancelled(
                "Cancellation requested by {} token".format(self.triggered_token)
            )
        return done.pop().result()

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return '<CancelToken: {0}>'.format(self.name)
