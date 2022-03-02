function X=tro_select_sol(Xq_old,Xq,X)

% Resolve the sign ambiguity for the TRO problem.

% Author: Cem Musluoglu, KU Leuven, Department of Electrical Engineering
% (ESAT), STADIUS Center for Dynamical Systems, Signal Processing and Data
% Analytics
% Correspondence: cemates.musluoglu@esat.kuleuven.be

    Q=size(Xq_old,2);

    for l=1:Q
        if norm(Xq_old(:,l)-Xq(:,l))>norm(-Xq_old(:,l)-Xq(:,l))
            X(:,l)=-X(:,l);
        end
    end

end