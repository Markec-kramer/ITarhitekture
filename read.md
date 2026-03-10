# Microservice System

Projekt predstavlja mikrostoritveni sistem za rezervacijo športnih igrišč, razvit v okviru laboratorijskih vaj.

## Namen
Cilj projekta je razviti sistem, sestavljen iz treh mikrostoritev in spletne aplikacije, pri čemer arhitektura sledi načelom Clean Architecture.

## Arhitektura
Sistem sestavljajo naslednje komponente:
- users
- courts
- reservations
- booking-portal

Sistem sestavljajo:
- Users – upravljanje uporabnikov
- Courts – upravljanje športnih igrišč
- Reservations – ustvarjanje in pregled rezervacij
- Booking Portal – uporabniški vmesnik

Storitve komunicirajo prek HTTP API-jev.

Vsaka storitev je ločena enota z jasno definirano odgovornostjo.

## Struktura repozitorija
- `users/` – upravljanje uporabnikov
- `courts/` – upravljanje športnih igrišč
- `reservations/` – rezervacija terminov
- `booking-portal/` – spletni uporabniški vmesnik
- `docs/` – dodatna dokumentacija

## Arhitekturna načela
Projekt sledi:
- Clean Architecture
- ohlapni sklopljenosti med storitvami
- neodvisnosti domene od infrastrukture
- screaming architecture pristopu

