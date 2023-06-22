import asyncio

from ParserInterface import ParserMiddleware

from Parsers.Services.VKParser import VKGroupParser

# https://regvk.com/id/

target = "201880129"


async def main():
    await asyncio.gather(
        ParserMiddleware.parse_until_date(
            instance=VKGroupParser(), until_date="2023-06-21 00:00:00", target=target
        ),
        ParserMiddleware.parse_until_id(
            instance=VKGroupParser(), until_id=333624, target=target
        ),
        # ParserMiddleware.parse_all(
        #     instance=VKGroupParser(),
        #     target=target
        # )
    )


asyncio.run(main())
