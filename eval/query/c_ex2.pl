% db("music.db"). func(f1). func(f2).
% trc_sql(p_,I,T) :- trc_sql(p,I,T), graph(p,I,_).
% graph(call(f2,call(f1),I),I,O) :- graph(p,I,O).

% Guiding facts
db("music.db"). func(f1). func(f2). % Just provided to the LLM as context, not used in the in this example.

% Base program facts
program(p).
program(p_).
language(p, javascript).

% Plugin-provided facts
can(graph(P)) :- language(P, javascript).
can(trc_sql(P)) :- language(P, javascript).

can(trc_sql(p,trc_sql_p_I,trc_sql_p_T)) :- do(trc_sql(P)), do(graph(p,trc_sql_p_I, _)), program(P).
can(graph(P, trc_sql_p_I, anonV_xyz)) :- do(graph(P)), program(P).
can(graph(P, graph_p_I, graph_p_O)) :- do(graph(P)), program(P).

can(trc_sql(p_,trc_sql_p_I,trc_sql_p_T)) :- do(trc_sql(p,trc_sql_p_I,trc_sql_p_T)), do(graph(p,trc_sql_p_I,_)).
can(graph(call(f2,call(f1),graph_p_I),graph_p_I,graph_p_O)) :- do(graph(p, graph_p_I, graph_p_O)).

% Axioms
:- do(language(P, L1)), language(P, _). % Cannot have multiple languages for the same program.

0 { do(X) } 1 :- can(X).
% -------

:- not do(graph(call(f2,call(f1),graph_p_I),graph_p_I,graph_p_O)).

#show do/1.
