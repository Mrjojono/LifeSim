(define (domain ecosystem)
  (:requirements :strips :typing)
  (:types cell)

  (:predicates
    (at ?c - cell)            ; Position de l'agent
    (neighbor ?c1 ?c2 - cell)   ; Adjacence (H, B, G, D)
    (is-virus ?c - cell)       ; Présence d'un virus rouge
    (is-empty ?c - cell)       ; Case saine ou vide
  )

  ; Action 1 : Se déplacer
  ; L'agent peut se déplacer sur n'importe quelle case voisine
  (:action move
    :parameters (?from - cell ?to - cell)
    :precondition (and (at ?from) (neighbor ?from ?to))
    :effect (and (not (at ?from)) (at ?to))
  )

  ; Action 2 : Soigner (Cure)
  ; L'agent soigne une case VOISINE qui contient un virus
  (:action cure
    :parameters (?agent_pos - cell ?virus_pos - cell)
    :precondition (and (at ?agent_pos) (neighbor ?agent_pos ?virus_pos) (is-virus ?virus_pos))
    :effect (and (not (is-virus ?virus_pos)) (is-empty ?virus_pos))
  )
)