import os
import sys
from streamlit.testing.v1 import AppTest

def test_wheat_seeds_app():
    dep_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dep_dir)
    print(f"Testing app.py in: {dep_dir}")

    # 1. Profil 1 : Graine compacte / petit gabarit (Cluster 0 attendu)
    at1 = AppTest.from_file("app.py", default_timeout=30)
    at1.run()
    assert len(at1.exception) == 0, f"Exception initialisation 1 : {at1.exception}"

    at1.number_input[0].set_value(12.0)
    at1.number_input[1].set_value(13.0)
    at1.number_input[2].set_value(0.850)
    at1.number_input[3].set_value(5.0)
    at1.number_input[4].set_value(2.9)
    at1.number_input[5].set_value(3.5)
    at1.number_input[6].set_value(4.8)

    at1.button[0].click().run()
    assert len(at1.exception) == 0, f"Exception prédiction 1 : {at1.exception}"
    assert len(at1.info) > 0 or len(at1.success) > 0, "Aucun message de cluster trouvé pour test 1"
    res1 = at1.info[0].value if len(at1.info) > 0 else at1.success[0].value
    print(f"Résultat Test 1 : {res1}")

    # 2. Profil 2 : Graine volumineuse / grand gabarit (Cluster 1 attendu)
    at2 = AppTest.from_file("app.py", default_timeout=30)
    at2.run()
    assert len(at2.exception) == 0, f"Exception initialisation 2 : {at2.exception}"

    at2.number_input[0].set_value(19.0)
    at2.number_input[1].set_value(16.5)
    at2.number_input[2].set_value(0.890)
    at2.number_input[3].set_value(6.3)
    at2.number_input[4].set_value(3.8)
    at2.number_input[5].set_value(4.0)
    at2.number_input[6].set_value(6.2)

    at2.button[0].click().run()
    assert len(at2.exception) == 0, f"Exception prédiction 2 : {at2.exception}"
    assert len(at2.info) > 0 or len(at2.success) > 0, "Aucun message de cluster trouvé pour test 2"
    res2 = at2.info[0].value if len(at2.info) > 0 else at2.success[0].value
    print(f"Résultat Test 2 : {res2}")

    assert res1 != res2, f"Les clusters attribués sont identiques : {res1}"
    print("SUCCESS: Wheat seeds app test passed with 0 exception and two different clusters!")

if __name__ == "__main__":
    test_wheat_seeds_app()
