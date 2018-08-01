import pytest
from mock import patch
import database
from drop_branch import DropBranch
from sdk.branch_link import BranchLink
from sdk.branch import Branch
from model.domain import conta
from uuid import uuid4
from sqlalchemy import text


def get_branch_link():
    return [
        {
            "_metadata": {
                "branch": "master",
                "modified_at": "2018-05-24T14:15:54.116590",
                "type": "branchLink"
            },
            "branchName": "cenario-01",
            "entity": "conta",
            "id": "50793d75-a8ee-41f8-b16e-36c5368c253d",
            "systemId": "ec498841-59e5-47fd-8075-136d79155705"
        }
    ]

def test_should_drop(session):
    #Arrange
    c = conta(titular="moneda", saldo=0, id=str(uuid4()))
    session.add(c)
    session.commit()
    conta_branch = conta(titular="moneda", saldo=5, id=c.id, from_id=c.rid, branch="cenario-01")
    conta_branch_2 = conta(titular="moneda", saldo=15, id=c.id, branch="cenario-01")
    session.add(conta_branch_2)
    session.add(conta_branch)
    session.commit()

    with patch.object(BranchLink, 'get', return_value=get_branch_link()) as mock_branch_link:
        with patch.object(Branch, 'set_dropped', return_value=[]) as mock_branch:
            drop = DropBranch(session)

            #Act
            drop.drop("cenario-01","user")
            #Assert
            mock_branch_link.assert_called()
            mock_branch.assert_called_with("cenario-01","user")
            old_branch = session.query(conta).filter(text("branch = 'cenario-01'")).all()
            assert len(old_branch) == 0
            history_branch = session.query(conta).filter(text("branch = 'dropped:cenario-01'")).all()
            assert len(history_branch) == 2