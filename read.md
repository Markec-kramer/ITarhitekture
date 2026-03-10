# Microservice System

Projekt predstavlja mikrostoritveni sistem za izposojo vozil (avtomobili, kombiji, motorji), razvit v okviru laboratorijskih vaj.

## Namen
Cilj projekta je razviti sistem, ki uporabnikom omogoča pregled razpoložljivih vozil v različnih poslovalnicah ter rezervacijo vozila za določen čas. Uporabniki lahko preverijo, kateri modeli vozil so na voljo v posamezni poslovalnici in primerjajo cene najema glede na trajanje izposoje.

Sistem je sestavljen iz treh mikrostoritev in spletne aplikacije, pri čemer arhitektura sledi načelom Clean Architecture.

## Arhitektura
Sistem sestavljajo naslednje komponente:
- users
- vehicles
- reservations
- rental-portal

Sistem sestavljajo:
- Users – upravljanje uporabnikov
- Vehicles – upravljanje vozil, njihovih modelov in poslovalnic
- Reservations – ustvarjanje in pregled rezervacij vozil
- Rental Portal – uporabniški vmesnik

Storitve komunicirajo prek HTTP API-jev.

Vsaka storitev je ločena enota z jasno definirano odgovornostjo.

## Struktura repozitorija
- `users/` – upravljanje uporabnikov
- `vehicles/` – upravljanje vozil, modelov in poslovalnic
- `reservations/` – rezervacija vozil za določen čas
- `rental-portal/` – spletni uporabniški vmesnik
- `docs/` – dodatna dokumentacija

## Arhitekturna načela
Projekt sledi:
- Clean Architecture
- ohlapni sklopljenosti med storitvami
- neodvisnosti domene od infrastrukture
- screaming architecture pristopu