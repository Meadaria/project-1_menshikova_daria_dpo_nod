install:
	poetry install

project:
	poetry run python -m labyrinth_game.main

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python -m pip install dist/project_1_menshikova_daria_dpo_nod-0.1.0-py3-none-any.whl