% the number of pararell counts
parpool('local', 2);

% hyper parameter
K = 10;
alpha = 20;
max_iter = 15;
topk = 10;

% city indexing
Buda = 0;
Delh = 1;
Edin = 2;
Glas = 3;
Osak = 4;
Pert = 5;
Toro = 6;
Vien = 7;
Kyoto = 8;

result_file_name = 'result.csv';

%-------------------------
% Buda: 0
%-------------------------
% read data
data = readContent('./sightseeing/data-Buda-allPOI.txt', 'zero_start',true);

% test ratio 0.2
test_ratio = 0.2;
[summary, detail, elapsed] = item_recommend(@(mat) geomf(mat, 'alpha', alpha, 'K', K, 'max_iter', max_iter), data, 'topk', topk, 'test_ratio', test_ratio);
result_array = [summary.item_prec_like(1, 1), summary.item_prec_like(1, 5), summary.item_prec_like(1, 10), summary.item_recall_like(1, 1), summary.item_recall_like(1, 5), summary.item_recall_like(1, 10)];
dlmwrite(result_file_name, [Buda, test_ratio, result_array], '-append')
% test ratio 0.5
test_ratio = 0.5;
[summary, detail, elapsed] = item_recommend(@(mat) geomf(mat, 'alpha', alpha, 'K', K, 'max_iter', max_iter), data, 'topk', topk, 'test_ratio', test_ratio);
result_array = [summary.item_prec_like(1, 1), summary.item_prec_like(1, 5), summary.item_prec_like(1, 10), summary.item_recall_like(1, 1), summary.item_recall_like(1, 5), summary.item_recall_like(1, 10)];
dlmwrite(result_file_name, [Buda, test_ratio, result_array], '-append')
% test ratio 0.8
test_ratio = 0.8;
[summary, detail, elapsed] = item_recommend(@(mat) geomf(mat, 'alpha', alpha, 'K', K, 'max_iter', max_iter), data, 'topk', topk, 'test_ratio', test_ratio);
result_array = [summary.item_prec_like(1, 1), summary.item_prec_like(1, 5), summary.item_prec_like(1, 10), summary.item_recall_like(1, 1), summary.item_recall_like(1, 5), summary.item_recall_like(1, 10)];
dlmwrite(result_file_name, [Buda, test_ratio, result_array], '-append')

%-------------------------
% Delh: 1
%-------------------------
% read data 
data = readContent('./sightseeing/data-Delh-allPOI.txt', 'zero_start',true);

% test ratio 0.2
test_ratio = 0.2;
[summary, detail, elapsed] = item_recommend(@(mat) geomf(mat, 'alpha', alpha, 'K', K, 'max_iter', max_iter), data, 'topk', topk, 'test_ratio', test_ratio);
result_array = [summary.item_prec_like(1, 1), summary.item_prec_like(1, 5), summary.item_prec_like(1, 10), summary.item_recall_like(1, 1), summary.item_recall_like(1, 5), summary.item_recall_like(1, 10)];
dlmwrite(result_file_name, [Delh, test_ratio, result_array], '-append')
% test ratio 0.5
test_ratio = 0.5;
[summary, detail, elapsed] = item_recommend(@(mat) geomf(mat, 'alpha', alpha, 'K', K, 'max_iter', max_iter), data, 'topk', topk, 'test_ratio', test_ratio);
result_array = [summary.item_prec_like(1, 1), summary.item_prec_like(1, 5), summary.item_prec_like(1, 10), summary.item_recall_like(1, 1), summary.item_recall_like(1, 5), summary.item_recall_like(1, 10)];
dlmwrite(result_file_name, [Delh, test_ratio, result_array], '-append')
% test ratio 0.8
test_ratio = 0.8;
[summary, detail, elapsed] = item_recommend(@(mat) geomf(mat, 'alpha', alpha, 'K', K, 'max_iter', max_iter), data, 'topk', topk, 'test_ratio', test_ratio);
result_array = [summary.item_prec_like(1, 1), summary.item_prec_like(1, 5), summary.item_prec_like(1, 10), summary.item_recall_like(1, 1), summary.item_recall_like(1, 5), summary.item_recall_like(1, 10)];
dlmwrite(result_file_name, [Delh, test_ratio, result_array], '-append')

%-------------------------
% Edin: 2
%-------------------------
% read data Edin
data = readContent('./sightseeing/data-Edin.txt', 'zero_start',true);

% test ratio 0.2
test_ratio = 0.2;
[summary, detail, elapsed] = item_recommend(@(mat) geomf(mat, 'alpha', alpha, 'K', K, 'max_iter', max_iter), data, 'topk', topk, 'test_ratio', test_ratio);
result_array = [summary.item_prec_like(1, 1), summary.item_prec_like(1, 5), summary.item_prec_like(1, 10), summary.item_recall_like(1, 1), summary.item_recall_like(1, 5), summary.item_recall_like(1, 10)];
dlmwrite(result_file_name, [Edin, test_ratio, result_array], '-append')
% test ratio 0.5
test_ratio = 0.5;
[summary, detail, elapsed] = item_recommend(@(mat) geomf(mat, 'alpha', alpha, 'K', K, 'max_iter', max_iter), data, 'topk', topk, 'test_ratio', test_ratio);
result_array = [summary.item_prec_like(1, 1), summary.item_prec_like(1, 5), summary.item_prec_like(1, 10), summary.item_recall_like(1, 1), summary.item_recall_like(1, 5), summary.item_recall_like(1, 10)];
dlmwrite(result_file_name, [Edin, test_ratio, result_array], '-append')
% test ratio 0.8
test_ratio = 0.8;
[summary, detail, elapsed] = item_recommend(@(mat) geomf(mat, 'alpha', alpha, 'K', K, 'max_iter', max_iter), data, 'topk', topk, 'test_ratio', test_ratio);
result_array = [summary.item_prec_like(1, 1), summary.item_prec_like(1, 5), summary.item_prec_like(1, 10), summary.item_recall_like(1, 1), summary.item_recall_like(1, 5), summary.item_recall_like(1, 10)];
dlmwrite(result_file_name, [Edin, test_ratio, result_array], '-append')

%-------------------------
% Glas: 3
%-------------------------
% read data
data = readContent('./sightseeing/data-Glas.txt', 'zero_start',true);

% test ratio 0.2
test_ratio = 0.2;
[summary, detail, elapsed] = item_recommend(@(mat) geomf(mat, 'alpha', alpha, 'K', K, 'max_iter', max_iter), data, 'topk', topk, 'test_ratio', test_ratio);
result_array = [summary.item_prec_like(1, 1), summary.item_prec_like(1, 5), summary.item_prec_like(1, 10), summary.item_recall_like(1, 1), summary.item_recall_like(1, 5), summary.item_recall_like(1, 10)];
dlmwrite(result_file_name, [Glas, test_ratio, result_array], '-append')
% test ratio 0.5
test_ratio = 0.5;
[summary, detail, elapsed] = item_recommend(@(mat) geomf(mat, 'alpha', alpha, 'K', K, 'max_iter', max_iter), data, 'topk', topk, 'test_ratio', test_ratio);
result_array = [summary.item_prec_like(1, 1), summary.item_prec_like(1, 5), summary.item_prec_like(1, 10), summary.item_recall_like(1, 1), summary.item_recall_like(1, 5), summary.item_recall_like(1, 10)];
dlmwrite(result_file_name, [Glas, test_ratio, result_array], '-append')
% test ratio 0.8
test_ratio = 0.8;
[summary, detail, elapsed] = item_recommend(@(mat) geomf(mat, 'alpha', alpha, 'K', K, 'max_iter', max_iter), data, 'topk', topk, 'test_ratio', test_ratio);
result_array = [summary.item_prec_like(1, 1), summary.item_prec_like(1, 5), summary.item_prec_like(1, 10), summary.item_recall_like(1, 1), summary.item_recall_like(1, 5), summary.item_recall_like(1, 10)];
dlmwrite(result_file_name, [Glas, test_ratio, result_array], '-append')

%-------------------------
% Osak: 4
%-------------------------
% read data
data = readContent('./sightseeing/data-Osak.txt', 'zero_start',true);

% test ratio 0.2
test_ratio = 0.2;
[summary, detail, elapsed] = item_recommend(@(mat) geomf(mat, 'alpha', alpha, 'K', K, 'max_iter', max_iter), data, 'topk', topk, 'test_ratio', test_ratio);
result_array = [summary.item_prec_like(1, 1), summary.item_prec_like(1, 5), summary.item_prec_like(1, 10), summary.item_recall_like(1, 1), summary.item_recall_like(1, 5), summary.item_recall_like(1, 10)];
dlmwrite(result_file_name, [Osak, test_ratio, result_array], '-append')
% test ratio 0.5
test_ratio = 0.5;
[summary, detail, elapsed] = item_recommend(@(mat) geomf(mat, 'alpha', alpha, 'K', K, 'max_iter', max_iter), data, 'topk', topk, 'test_ratio', test_ratio);
result_array = [summary.item_prec_like(1, 1), summary.item_prec_like(1, 5), summary.item_prec_like(1, 10), summary.item_recall_like(1, 1), summary.item_recall_like(1, 5), summary.item_recall_like(1, 10)];
dlmwrite(result_file_name, [Osak, test_ratio, result_array], '-append')
% test ratio 0.8
test_ratio = 0.8;
[summary, detail, elapsed] = item_recommend(@(mat) geomf(mat, 'alpha', alpha, 'K', K, 'max_iter', max_iter), data, 'topk', topk, 'test_ratio', test_ratio);
result_array = [summary.item_prec_like(1, 1), summary.item_prec_like(1, 5), summary.item_prec_like(1, 10), summary.item_recall_like(1, 1), summary.item_recall_like(1, 5), summary.item_recall_like(1, 10)];
dlmwrite(result_file_name, [Osak, test_ratio, result_array], '-append')

%-------------------------
% Pert: 5
%-------------------------
% read data
data = readContent('./sightseeing/data-Pert-allPOI.txt', 'zero_start',true);

% test ratio 0.2
test_ratio = 0.2;
[summary, detail, elapsed] = item_recommend(@(mat) geomf(mat, 'alpha', alpha, 'K', K, 'max_iter', max_iter), data, 'topk', topk, 'test_ratio', test_ratio);
result_array = [summary.item_prec_like(1, 1), summary.item_prec_like(1, 5), summary.item_prec_like(1, 10), summary.item_recall_like(1, 1), summary.item_recall_like(1, 5), summary.item_recall_like(1, 10)];
dlmwrite(result_file_name, [Pert, test_ratio, result_array], '-append')
% test ratio 0.5
test_ratio = 0.5;
[summary, detail, elapsed] = item_recommend(@(mat) geomf(mat, 'alpha', alpha, 'K', K, 'max_iter', max_iter), data, 'topk', topk, 'test_ratio', test_ratio);
result_array = [summary.item_prec_like(1, 1), summary.item_prec_like(1, 5), summary.item_prec_like(1, 10), summary.item_recall_like(1, 1), summary.item_recall_like(1, 5), summary.item_recall_like(1, 10)];
dlmwrite(result_file_name, [Pert, test_ratio, result_array], '-append')
% test ratio 0.8
test_ratio = 0.8;
[summary, detail, elapsed] = item_recommend(@(mat) geomf(mat, 'alpha', alpha, 'K', K, 'max_iter', max_iter), data, 'topk', topk, 'test_ratio', test_ratio);
result_array = [summary.item_prec_like(1, 1), summary.item_prec_like(1, 5), summary.item_prec_like(1, 10), summary.item_recall_like(1, 1), summary.item_recall_like(1, 5), summary.item_recall_like(1, 10)];
dlmwrite(result_file_name, [Pert, test_ratio, result_array], '-append')

%-------------------------
% Toro: 6
%-------------------------
% read data 
data = readContent('./sightseeing/data-Toro.txt', 'zero_start',true);

% test ratio 0.2
test_ratio = 0.2;
[summary, detail, elapsed] = item_recommend(@(mat) geomf(mat, 'alpha', alpha, 'K', K, 'max_iter', max_iter), data, 'topk', topk, 'test_ratio', test_ratio);
result_array = [summary.item_prec_like(1, 1), summary.item_prec_like(1, 5), summary.item_prec_like(1, 10), summary.item_recall_like(1, 1), summary.item_recall_like(1, 5), summary.item_recall_like(1, 10)];
dlmwrite(result_file_name, [Toro, test_ratio, result_array], '-append')
% test ratio 0.5
test_ratio = 0.5;
[summary, detail, elapsed] = item_recommend(@(mat) geomf(mat, 'alpha', alpha, 'K', K, 'max_iter', max_iter), data, 'topk', topk, 'test_ratio', test_ratio);
result_array = [summary.item_prec_like(1, 1), summary.item_prec_like(1, 5), summary.item_prec_like(1, 10), summary.item_recall_like(1, 1), summary.item_recall_like(1, 5), summary.item_recall_like(1, 10)];
dlmwrite(result_file_name, [Toro, test_ratio, result_array], '-append')
% test ratio 0.8
test_ratio = 0.8;
[summary, detail, elapsed] = item_recommend(@(mat) geomf(mat, 'alpha', alpha, 'K', K, 'max_iter', max_iter), data, 'topk', topk, 'test_ratio', test_ratio);
result_array = [summary.item_prec_like(1, 1), summary.item_prec_like(1, 5), summary.item_prec_like(1, 10), summary.item_recall_like(1, 1), summary.item_recall_like(1, 5), summary.item_recall_like(1, 10)];
dlmwrite(result_file_name, [Toro, test_ratio, result_array], '-append')

%-------------------------
% Vien: 7
%-------------------------
% read data 
data = readContent('./sightseeing/data-Vien-allPOI.txt', 'zero_start',true);

% test ratio 0.2
test_ratio = 0.2;
[summary, detail, elapsed] = item_recommend(@(mat) geomf(mat, 'alpha', alpha, 'K', K, 'max_iter', max_iter), data, 'topk', topk, 'test_ratio', test_ratio);
result_array = [summary.item_prec_like(1, 1), summary.item_prec_like(1, 5), summary.item_prec_like(1, 10), summary.item_recall_like(1, 1), summary.item_recall_like(1, 5), summary.item_recall_like(1, 10)];
dlmwrite(result_file_name, [Vien, test_ratio, result_array], '-append')
% test ratio 0.5
test_ratio = 0.5;
[summary, detail, elapsed] = item_recommend(@(mat) geomf(mat, 'alpha', alpha, 'K', K, 'max_iter', max_iter), data, 'topk', topk, 'test_ratio', test_ratio);
result_array = [summary.item_prec_like(1, 1), summary.item_prec_like(1, 5), summary.item_prec_like(1, 10), summary.item_recall_like(1, 1), summary.item_recall_like(1, 5), summary.item_recall_like(1, 10)];
dlmwrite(result_file_name, [Vien, test_ratio, result_array], '-append')
% test ratio 0.8
test_ratio = 0.8;
[summary, detail, elapsed] = item_recommend(@(mat) geomf(mat, 'alpha', alpha, 'K', K, 'max_iter', max_iter), data, 'topk', topk, 'test_ratio', test_ratio);
result_array = [summary.item_prec_like(1, 1), summary.item_prec_like(1, 5), summary.item_prec_like(1, 10), summary.item_recall_like(1, 1), summary.item_recall_like(1, 5), summary.item_recall_like(1, 10)];
dlmwrite(result_file_name, [Vien, test_ratio, result_array], '-append')

%-------------------------
% Kyoto: 8
%-------------------------
% read data
data = readContent('./sightseeing/data-kyoto.txt', 'zero_start',true);
% test ratio 0.2
test_ratio = 0.2;
[summary, detail, elapsed] = item_recommend(@(mat) geomf(mat, 'alpha', alpha, 'K', K, 'max_iter', max_iter), data, 'topk', topk, 'test_ratio', test_ratio);
result_array = [summary.item_prec_like(1, 1), summary.item_prec_like(1, 5), summary.item_prec_like(1, 10), summary.item_recall_like(1, 1), summary.item_recall_like(1, 5), summary.item_recall_like(1, 10)];
dlmwrite(result_file_name, [Kyoto, test_ratio, result_array], '-append')
% test ratio 0.5
test_ratio = 0.5;
[summary, detail, elapsed] = item_recommend(@(mat) geomf(mat, 'alpha', alpha, 'K', K, 'max_iter', max_iter), data, 'topk', topk, 'test_ratio', test_ratio);
result_array = [summary.item_prec_like(1, 1), summary.item_prec_like(1, 5), summary.item_prec_like(1, 10), summary.item_recall_like(1, 1), summary.item_recall_like(1, 5), summary.item_recall_like(1, 10)];
dlmwrite(result_file_name, [Kyoto, test_ratio, result_array], '-append')
% test ratio 0.8
test_ratio = 0.8;
[summary, detail, elapsed] = item_recommend(@(mat) geomf(mat, 'alpha', alpha, 'K', K, 'max_iter', max_iter), data, 'topk', topk, 'test_ratio', test_ratio);
result_array = [summary.item_prec_like(1, 1), summary.item_prec_like(1, 5), summary.item_prec_like(1, 10), summary.item_recall_like(1, 1), summary.item_recall_like(1, 5), summary.item_recall_like(1, 10)];
dlmwrite(result_file_name, [Kyoto, test_ratio, result_array], '-append')
