# Установка переменных среды для Java
$Env:JAVA_HOME = "C:\Program Files\Java\jdk-23"
$Env:Path += ";C:\Program Files\Java\jdk-23\bin"

# Запуск Allure для отображения отчета
& "C:\allure-2.30.0\bin\allure.bat" serve allure-results
