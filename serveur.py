from http.server import BaseHTTPRequestHandler
import argparse
import asyncio
import sys
from aiohttp import web

async def run_command(*args):
    process = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    return stdout.decode().strip()

async def handle(request):
    ip = request.match_info.get('ip', "")
    if ip == "":
        return ip
    else:

        commands = run_command('nmap', '-sV', ip)
        result = await commands
        text = str(format(result))
    return web.Response(text=text)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port")

    parser.add_argument("--host")

    args = parser.parse_args()

    print(int(args.port), args.host)
    app = web.Application()
    app.router.add_get('/{ip}', handle)

    web.run_app(app, host=args.host, port=int(args.port))

main()