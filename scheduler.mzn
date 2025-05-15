include "globals.mzn";

int: NumGames;
int: NumReferees;
int: NumFields;

array[1..NumGames] of int: game_id;
array[1..NumGames] of int: game_start;
array[1..NumGames] of int: game_end;
array[1..NumGames] of int: difficulty;
array[1..NumGames] of int: game_field;

array[1..NumReferees] of int: referee_id;
array[1..NumReferees] of int: main_exp;
array[1..NumReferees] of int: assist_exp;

% Each referee may have up to 3 availability intervals (from, to)
array[1..NumReferees, 1..3, 1..2] of int: available_slots;

% Decision variables: which referee is assigned to each role in each game
array[1..NumGames] of var 1..NumReferees: main_ref;
array[1..NumGames, 1..2] of var 1..NumReferees: assistant_ref;
array[1..NumGames] of var 1..NumReferees: fourth_official;

% Constraint: All 4 roles in a match must be assigned to different referees
constraint forall(g in 1..NumGames)(
    main_ref[g] != assistant_ref[g,1] /\
    main_ref[g] != assistant_ref[g,2] /\
    main_ref[g] != fourth_official[g] /\
    assistant_ref[g,1] != assistant_ref[g,2] /\
    assistant_ref[g,1] != fourth_official[g] /\
    assistant_ref[g,2] != fourth_official[g]
);

% Helper predicate: checks if referee r is available during [t_start, t_end]
predicate is_available(var int: r, var int: t_start, var int: t_end) =
    exists(i in 1..3) (
        let {
            var int: from_time = available_slots[r,i,1],
            var int: to_time   = available_slots[r,i,2]
        } in
            from_time <= t_start /\ to_time >= t_end
    );

% Constraint: All assigned referees must be available for the game time
constraint forall(g in 1..NumGames)(
    is_available(main_ref[g], game_start[g], game_end[g]) /\
    is_available(assistant_ref[g,1], game_start[g], game_end[g]) /\
    is_available(assistant_ref[g,2], game_start[g], game_end[g]) /\
    is_available(fourth_official[g], game_start[g], game_end[g])
);

% Constraint: One referee can only be assigned for one game at the same time
constraint
  forall(g1 in 1..NumGames, g2 in g1+1..NumGames
    where game_start[g1] < game_end[g2]
      /\ game_start[g2] < game_end[g1]
  ) (
    all_different([
      main_ref[g1],    assistant_ref[g1,1], assistant_ref[g1,2], fourth_official[g1],
      main_ref[g2],    assistant_ref[g2,1], assistant_ref[g2,2], fourth_official[g2]
    ])
  );

% Role Fatigue Limit
constraint
  forall(r in 1..NumReferees)(
    count([main_ref[g] = r | g in 1..NumGames]) +
    count([assistant_ref[g,a] = r | g in 1..NumGames, a in 1..2]) <= 2
  );

% Traveling Time Contraint
constraint
  forall(g1 in 1..NumGames, g2 in 1..NumGames where g1 != g2)(
    forall(r in 1..NumReferees)(
      let {
        var bool: assigned_both =
          (main_ref[g1] = r \/ assistant_ref[g1,1] = r \/ assistant_ref[g1,2] = r) /\
          (main_ref[g2] = r \/ assistant_ref[g2,1] = r \/ assistant_ref[g2,2] = r),
        bool: different_fields = game_field[g1] != game_field[g2],
        int: gap1 = game_start[g2] - game_end[g1],
        int: gap2 = game_start[g1] - game_end[g2]
      } in
      assigned_both /\ different_fields ->
        (gap1 >= 30 \/ gap2 >= 30)
    )
  );

% Objective: Maximize the quality of assignments
% Quality = difficulty * experience for main and assistant referees
var int: quality_score =
    sum(g in 1..NumGames)(
        difficulty[g] * main_exp[main_ref[g]] +
        difficulty[g] * assist_exp[assistant_ref[g,1]] +
        difficulty[g] * assist_exp[assistant_ref[g,2]]
    );

solve maximize quality_score;

output
[
  "Game assignments:\n"
]
++
[
  "Game " ++ show(game_id[g]) ++
  ": Main: " ++ show(referee_id[main_ref[g]]) ++
  ", Assistants: " ++ show(referee_id[assistant_ref[g,1]]) ++
  ", " ++ show(referee_id[assistant_ref[g,2]]) ++
  ", Fourth Official: " ++ show(referee_id[fourth_official[g]]) ++
  "\n"
  | g in 1..NumGames
]
++
[
  "Total score: " ++ show(quality_score) ++ "\n"
];
