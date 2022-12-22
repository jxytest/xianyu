import frida


def on_message(message, data):
    print(message)


if __name__ == '__main__':
    device = frida.get_remote_device()
    pid = device.attach('闲鱼')
    with open('rpc_dev.js', encoding='utf-8') as f:
        source = f.read()
    script = pid.create_script(source)
    script.on('message', on_message)
    script.load()
    script.exports.getSign2('{"a":1}', '{"b":2}')
