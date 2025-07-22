% graph(p_, Ih, Oh) :- graph(p, Ijs, Ojs), tr(Ijs, Ih), tr(Ojs, Oh).
% language(p_, haskell).

% Base program facts
program(p).
program(p_).
language(p, javascript).

% Plugin-provided facts
can(graph(P)) :- language(P, javascript).
can(tr).
% ------------

can(graph(P, graph_p_Ijs, graph_p_Ojs)) :- do(graph(P)), program(P).
can(tr(graph_p_Ijs, tr_graph_p_Ijs_Ih)) :- do(tr), do(graph(P, graph_p_Ijs, graph_p_Ojs)), program(P).
can(tr(graph_p_Ojs, tr_graph_p_Ojs_Oh)) :- do(tr), do(graph(P, graph_p_Ijs, graph_p_Ojs)), program(P).

can(language(P, haskell)) :- program(P).

can(graph(p_, tr_graph_p_Ijs_Ih, tr_graph_p_Ojs_Oh)) :- do(graph(p, graph_p_Ijs, graph_p_Ojs)), 
                    do(tr(graph_p_Ijs, tr_graph_p_Ijs_Ih)), do(tr(graph_p_Ojs, tr_graph_p_Ojs_Oh)).

% Axioms
:- do(language(P, L1)), language(P, _). % Cannot have multiple languages for the same program.

0 { do(X) } 1 :- can(X).

:- not do(graph(p_, tr_graph_p_Ijs_Ih, tr_graph_p_Ojs_Oh)).
:- not do(language(p_, haskell)).

#show do/1.
