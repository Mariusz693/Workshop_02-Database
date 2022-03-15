# Warkshop_02-Database

W trakcie warsztatu stworzony został prosty serwer komunikatów, składający się z czterech części:

- skrypt budujący naszą bazę danych,
- biblioteka do zarządzania bazą danych,
- aplikacja do zarządzania użytkownikami,
- aplikacja do wysyłania wiadomości.

Skrypt budujący bazę danych
Prosty skrypt tworzący bazę danych i tabele. Wielokrotne wywołanie skryptu przynosi ten sam efekt. Działa niezależnie od tego, czy mamy już utworzoną bazę danych, czy nie, czy w bazie danych są jakieś tabele, czy nie.

Biblioteka do zarządzania bazą danych
Zbiór klas służący do zarządzania tabelami w bazie danych. W tym celu został wykorzystamy wzorzec projektowy Active Record.

Aplikacja do zarządzania użytkownikami
Prosta aplikacja konsolowa, do zarządzania użytkownikami. Obsługuje takie zadania, jak:
- listowanie użytkowników,
- tworzenie nowego użytkownika,
- zmiana hasła użytkownika,
- usuwanie użytkownika.
Aplikacja obsługuje parametry, przekazywane do niej z poziomu konsoli. Wykorzystuje do tego bibliotekę argparse.

Aplikacja do wysyłania wiadomości
Kolejna aplikacja konsolowa, umożliwiająca przesyłanie wiadomości między użytkownikami. Implementuje takie funkcjonalności, jak:
- wypisanie wszystkich komunikatów wysłanych do użytkownika,
- wysłanie wiadomości.
Ponadto sprawdza, czy podany użytkownik istnieje i czy hasło jest poprawne. Podobnie, jak w przypadku aplikacji do zarządzania użytkownika, obsługuje hasła, korzystając z biblioteki argparse.
