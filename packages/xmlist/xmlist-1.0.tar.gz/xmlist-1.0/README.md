# xmlist

`xmlist` is a module for generating XML, which it represents by lists and tuples.

## using xmlist

    xml = xmlist.serialize(['html',
        ('xmlns', 'http://www.w3.org/1999/xhtml'),
        ['head', ['title', 'Hello, world!']],
        ['body',
            ['h1', 'Hello, world!'],
            ['p', 'xmlist is a module for generating XML']]])

## hacking on xmlist

[assuming the setup\_requires and test\_requires are already installed with `pip --user`]

    virtualenv --python=python2.7 --system-site-packages env27 ;
    env27/bin/pip2 install --editable .

## testing xmlist

    env27/bin/python -B setup.py -q test
