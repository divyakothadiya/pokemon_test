# Pokémon Battle Simulator
## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd pokemon_battle


there are 3 endpoint as per below
1. get api/pokemon (including pagination: api/pokemon?page=2)
  "next": "<instance>/api/pokemon?page=3",
  "previous": "<instance>/api/pokemon?page=1",
2. post api/battle/   
3. get api/battle/<battle_id>
