import attr
from typing import Dict
from path import Path
import ruamel.yaml


@attr.s
class Config:
    repo_path: Path = attr.ib()
    users: Dict[str, str] = attr.ib(default={})
    public_access: bool = attr.ib(default=False)


def parse() -> Config:
    cfg_path = Path.getcwd() / "zpov.yml"
    parser = ruamel.yaml.YAML()
    parsed = parser.load(cfg_path.text())
    users = parsed["users"]
    repo_path = Path(parsed["repo_path"])
    public_access = parsed["public_access"]
    res = Config(users=users, repo_path=repo_path, public_access=public_access)
    return res
