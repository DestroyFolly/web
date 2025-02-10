all: ruff_check mypy_check clean pytest

.PHONY: all clean pytest
 
ruff_check: 
	ruff check .

ruff_fix:
	ruff --unsafe-fixes --fix check .

mypy_check:
	mypy .

unit_tests:
	pytest --alluredir=allure-results tests\user_tests.py tests\payment_tests.py tests\product_cart_tests.py tests\product_order_tests.py tests\cart_tests.py tests\order_tests.py tests\product_tests.py

integration_tests:
	pytest --alluredir=allure-results tests\integration_tests.py

e2e_tests:
	pytest --alluredir=allure-results tests\e2e.py



clean:
	rd /s /q .ruff_cache	
	rd /s /q .mypy_cache
