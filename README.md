# Стартовий проєкт: Практична робота 5

1. Відкрийте проєкт у GitHub Codespaces (Code → Codespaces → Create codespace) або локально: `python3 -m venv .venv`, `source .venv/bin/activate` (у Windows: `.venv\Scripts\activate`), `pip install -r requirements.txt`.
2. Визначте свою задачу за номером варіанта: задача = `(номер - 1) // 3 + 1`, набір = `(номер - 1) % 3 + 1`. Реалізуйте задачу у файлі `variants/variant_NN.py` за карткою.
3. Запускайте відкриті тести своєї задачі: `pytest tests/test_variant_NN.py` (NN з двома цифрами). Права адміністратора не потрібні.
4. Дані продуктових контекстів лежать у `data/` (файл вашого набору: `context_N_*.json`). Вони потрібні для прикладів, самостійних вправ і як навчальні кейси для частини Б.
5. Артефакт частини Б (ланцюжок DIBB і пітч Shape Up) складайте у `dibb/my_dibb.json`; формат показано в `dibb/format_example.json`; текстову версію пітчу напишіть у `dibb/pitch.md`. Перевірка: `pytest check -q` (змінна `DIBB` задає інший файл). Тести в `check/` не входять до `pytest tests`.
6. Змінюйте лише свій файл у `variants/`, файл `tests/test_my.py`, `dibb/my_dibb.json`, `dibb/pitch.md` і `ANSWERS.md`.
