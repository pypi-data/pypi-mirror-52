from __future__ import unicode_literals

import six

import pytest
import mock

from clldutils.path import copytree
from clldutils.clilib import ParserError

from pyglottolog.__main__ import commands


def _args(api_copy, *args):
    return mock.Mock(repos=api_copy, args=list(args), log=mock.Mock())


def test_no_repos(api):
    with pytest.raises(ParserError):
        commands.show(mock.Mock(repos=None, args=['abcd1235'], log=mock.Mock()))


def test_release(api_copy, mocker):
    mocker.patch('pyglottolog.commands.input', mocker.Mock(return_value='x.y'))
    with pytest.raises(ValueError):
        commands.release(_args(api_copy))
    mocker.patch('pyglottolog.commands.input', mocker.Mock(return_value='2.7'))
    commands.release(_args(api_copy))


def test_update_links(api_copy, capsys, elcat):
    commands.update_links(_args(api_copy, 'none'))
    out, _ = capsys.readouterr()
    assert '0 languoids updated' in out

    commands.update_links(_args(api_copy, 'elcat'))
    out, _ = capsys.readouterr()
    assert '1 languoids updated' in out


def test_show(capsys, api):
    commands.show(_args(api, '**a:key**'))
    assert (b'@misc' if six.PY2 else '@misc') in capsys.readouterr()[0]

    commands.show(_args(api, 'a:key'))
    assert (b'@misc' if six.PY2 else '@misc') in capsys.readouterr()[0]

    commands.show(_args(api, 'abcd1236'))
    assert (b'Classification' if six.PY2 else 'Classificat') in capsys.readouterr()[0]


def test_edit(mocker, api):
    mocker.patch('pyglottolog.commands.subprocess')
    commands.edit(_args(api, 'abcd1236'))


def test_create(capsys, api_copy):
    commands.create(_args(api_copy, 'abcd1234', 'new name', 'language'))
    assert 'Info written' in capsys.readouterr()[0]
    assert 'new name' in [c.name for c in api_copy.languoid('abcd1234').children]


def test_fts(capsys, api_copy):
    with pytest.raises(ValueError):
        commands.refsearch(_args(api_copy, 'Harzani year:1334'))

    commands.refindex(_args(api_copy))
    commands.refsearch(_args(api_copy, 'Harzani year:1334'))
    assert "'Abd-al-'Ali Karang" in capsys.readouterr()[0]

    commands.langindex(_args(api_copy))
    commands.langsearch(_args(api_copy, 'id:abcd*'))
    assert "abcd1234" in capsys.readouterr()[0]

    commands.langsearch(_args(api_copy, 'classification'))
    assert "abcd1234" in capsys.readouterr()[0]


def test_metadata(capsys, api):
    commands.metadata(_args(api))
    assert "longitude" in capsys.readouterr()[0]


def test_lff(capsys, api_copy, encoding='utf-8'):
    commands.tree2lff(_args(api_copy))

    dff = api_copy.build_path('dff.txt')
    dfftxt = dff.read_text(encoding=encoding).replace('dialect', 'Dialect Name')
    dff.write_text(dfftxt, encoding=encoding)
    commands.lff2tree(_args(api_copy))
    assert 'git status' in capsys.readouterr()[0]
    assert api_copy.languoid('abcd1236').name == 'Dialect Name'
    # Old language and dialect names are retained as alternative names:
    assert 'dialect' in api_copy.languoid('abcd1236').names['glottolog']

    commands.tree2lff(_args(api_copy))
    dfftxt = dff.read_text(encoding=encoding)


def test_index(api_copy):
    commands.index(_args(api_copy))
    assert len(list(api_copy.repos.joinpath('languoids').glob('*.md'))) == 10


def test_tree(capsys, api):
    with pytest.raises(commands.ParserError):
        commands.tree(_args(api))

    with pytest.raises(commands.ParserError):
        commands.tree(_args(api, 'xyz'))

    commands.tree(_args(api, 'abc', 'language'))
    out, _ = capsys.readouterr()
    if not isinstance(out, six.text_type):
        out = out.decode('utf-8')
    assert 'language' in out
    assert 'dialect' not in out


def test_languoids(capsys, api, tmpdir):
    commands.languoids(_args(api, '--output={0}'.format(tmpdir), '--version=1.5'))
    out, _ = capsys.readouterr()
    assert '-metadata.json' in out
    assert tmpdir.join('glottolog-languoids-1.5.csv').ensure()


def test_newick(capsys, api):
    commands.newick(_args(api, 'abcd1235'))
    assert 'language' in capsys.readouterr()[0]

    with pytest.raises(ParserError):
        commands.newick(_args(api, 'abcd123'))


def test_htmlmap(api, capsys, tmpdir):
    commands.htmlmap(_args(api, str(tmpdir)), min_langs_for_legend_item=1)
    out, _ = capsys.readouterr()
    assert 'glottolog_map.html' in out


def test_iso2codes(api, tmpdir):
    commands.iso2codes(_args(api, str(tmpdir)))
    assert tmpdir.join('iso2glottocodes.csv').check()


def test_roundtrip(api_copy):
    commands.roundtrip(_args(api_copy, 'a.bib'))


def test_bibfiles_db(api_copy):
    commands.bibfiles_db(_args(api_copy))


def test_update_sources(api_copy, capsys):
    commands.update_sources(_args(api_copy))
    out, _ = capsys.readouterr()
    assert '1 languoids updated' in out


def test_cldf(api_copy, tmpdir):
    commands._cldf(_args(api_copy, str(tmpdir.join('cldf'))))
    commands._cldf(_args(api_copy, str(tmpdir.join('cldf'))))


def test_check(capsys, api_copy):
    commands.check(_args(api_copy, 'refs'))

    args = _args(api_copy)
    commands.check(args)
    assert 'family' in capsys.readouterr()[0]
    msgs = [a[0] for a, _ in args.log.error.call_args_list]
    assert any('unregistered glottocode' in m for m in msgs)
    assert any('missing reference' in m for m in msgs)
    assert len(msgs) == 27

    copytree(
        api_copy.tree / 'abcd1234' / 'abcd1235',
        api_copy.tree / 'abcd1235')

    args = _args(api_copy)
    commands.check(args)
    msgs = [a[0] for a, _ in args.log.error.call_args_list]
    assert any('duplicate glottocode' in m for m in msgs)
    assert len(msgs) == 29

    (api_copy.tree / 'abcd1235').rename(api_copy.tree / 'abcd1237')
    args = _args(api_copy)
    commands.check(args)
    msgs = [a[0] for a, _ in args.log.error.call_args_list]
    assert any('duplicate hid' in m for m in msgs)
    assert len(msgs) >= 9


def test_check_2(api_copy, mocker, caplog):
    mocker.patch('pyglottolog.iso.check_lang', lambda _, i, l, **kw: ('warn', l, 'xyz'))
    commands.check(_args(api_copy, 'tree'))
    for record in caplog.records:
        print(record.message)


def test_monster(capsys, api_copy):
    commands.bib(_args(api_copy))
    assert capsys.readouterr()[0]
