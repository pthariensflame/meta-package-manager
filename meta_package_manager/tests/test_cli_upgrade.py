# Copyright Kevin Deldycke <kevin@deldycke.com> and contributors.
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

from __future__ import annotations

import pytest

from .conftest import default_manager_ids
from .test_cli import CLISubCommandTests, check_manager_selection


@pytest.fixture
def subcmd():
    return "upgrade", "--all"


class TestUpgrade(CLISubCommandTests):
    """All tests here should me marked as destructive unless --dry-run parameter is
    passed."""

    @pytest.mark.parametrize("all_option", ("--all", None))
    def test_all_managers_dry_run_upgrade_all(self, invoke, all_option):
        result = invoke("--dry-run", "upgrade", all_option)
        assert result.exit_code == 0
        if not all_option:
            assert "assume -A/--all option" in result.stderr
        check_manager_selection(result)

    @pytest.mark.destructive
    @pytest.mark.parametrize("all_option", ("--all", None))
    def test_all_managers_upgrade_all(self, invoke, all_option):
        result = invoke("upgrade", all_option)
        assert result.exit_code == 0
        if not all_option:
            assert "assume -A/--all option" in result.stderr
        check_manager_selection(result)

    @default_manager_ids
    @pytest.mark.parametrize("all_option", ("--all", None))
    def test_single_manager_dry_run_upgrade_all(self, invoke, manager_id, all_option):
        result = invoke(f"--{manager_id}", "--dry-run", "upgrade", all_option)
        assert result.exit_code == 0
        if not all_option:
            assert "assume -A/--all option" in result.stderr
        check_manager_selection(result, {manager_id})

    @pytest.mark.destructive
    @default_manager_ids
    @pytest.mark.parametrize("all_option", ("--all", None))
    def test_single_manager_upgrade_all(self, invoke, manager_id, all_option):
        result = invoke(f"--{manager_id}", "upgrade", all_option)
        assert result.exit_code == 0
        if not all_option:
            assert "assume -A/--all option" in result.stderr
        check_manager_selection(result, {manager_id})


pytest.mark.destructive()(TestUpgrade.test_stats)
pytest.mark.destructive()(TestUpgrade.test_manager_shortcuts)
pytest.mark.destructive()(TestUpgrade.test_manager_selection)
