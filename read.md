# Microservice System

Projekt predstavlja mikrostoritveni sistem, razvit v okviru laboratorijskih vaj.

## Namen
Cilj projekta je razviti sistem, sestavljen iz treh mikrostoritev in spletne aplikacije, pri čemer arhitektura sledi načelom Clean Architecture.

## Arhitektura
Sistem sestavljajo naslednje komponente:
- customer-management
- order-processing
- payment-handling
- customer-portal

Sistem sestavljajo:
- Guest Management – upravljanje gostov
- Reservation Management – ustvarjanje in pregled rezervacij
- Billing – obračun in plačila
- Web App – uporabniški vmesnik

Storitve komunicirajo prek HTTP API-jev.

Vsaka storitev je ločena enota z jasno definirano odgovornostjo.

## Struktura repozitorija
- `customer-management/` – upravljanje uporabnikov
- `order-processing/` – obdelava naročil
- `payment-handling/` – upravljanje plačil
- `customer-portal/` – spletni uporabniški vmesnik
- `docs/` – dodatna dokumentacija

## Arhitekturna načela
Projekt sledi:
- Clean Architecture
- ohlapni sklopljenosti med storitvami
- neodvisnosti domene od infrastrukture
- screaming architecture pristopu

## Status
Projekt je v razvoju.