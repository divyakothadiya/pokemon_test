# Pokémon Battle Simulator
## Setup for local

1. Clone the repository:
   ```bash
   git clone <repository-url:https://github.com/divyakothadiya/pokemon_test>
   cd pokemon_battle

2. Create and Activate Virtual Environment:
   create Environment: python -m venv myenv
   activate Environment: source myenv/bin/activate

3. Install Dependencies:
   pip install -r requirements.txt

4. Apply Migrations:
   python manage.py makemigrations
   python manage.py migrate

5. Load Pokemon Data from csv:
   python manage.py load_pokemon

6. Run the Development Server:
   python manage.py runserver

## Deployed on AWS server
There are 3 endpoint as per below
1. get api/pokemon (including pagination: api/pokemon?page=2)
  "next": "http://107.21.170.126:8001/api/pokemon?page=3",
  "previous": "http://107.21.170.126:8001/api/pokemon?page=1",
2. post http://107.21.170.126:8001/api/battle/   
3. get http://107.21.170.126:8001/api/battle/<battle_id>

## Postman collection 
https://api.postman.com/collections/33047892-d82a0592-0d91-4f2d-982e-854e001c4fa7?access_key=PMAT-01J4XMSR248MKJ9D934XZ974SA