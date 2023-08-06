# petrovna

Библиотека для валидации БИК, ИНН, КПП, ОГРН, ОГРНИП, Корр. счета, Номера р/с, СНИЛС

![coverage](https://git.appkode.ru/mozen/mz_validators/badges/master/coverage.svg?job=test)


Установка
```bash
pip install petrovna
```

```python
import petrovna

bic_is_valid: bool = petrovna.validate_bic('<БИК>')
inn_is_valid: bool  = petrovna.validate_inn('<ИНН>')
kpp_is_valid: bool  = petrovna.validate_kpp('<КПП>')
corr_account_is_valid: bool  = petrovna.validate_ks('<КОРРЕСПОНДЕНТСКИЙ_СЧЕТ>', '<БИК>')
ogrn_is_valid: bool  = petrovna.validate_ogrn('<ОГРН>')
ogrnip_is_valid: bool  = petrovna.validate_ogrnip('<ОГРНИП>')
account_number_is_valid: bool  = petrovna.validate_rs('<НОМЕР_Р/С>', '<БИК>')
snils_is_valid: bool  = petrovna.validate_snils('<СНИЛС>')

# Для возврата валидатором списка ошибок, помимо признака валидности, следует указать аргумент 'errors=True'
valid, error = petrovna.validate_bic('<БИК>', errors=True)
```