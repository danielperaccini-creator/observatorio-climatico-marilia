# Tarefas da próxima implementação

Responsável: Daniel Ricardo S. Peraccini (`danielperaccini-creator`).

O desenho v1 e a base técnica inicial foram preparados na mesma entrega. As sete issues abertas tratam da próxima implementação e da validação comunitária. Nenhuma devolutiva está registrada como concluída.

## [#1 - Preparar seleção de outro período de 30 dias](https://github.com/danielperaccini-creator/observatorio-climatico-marilia/issues/1)

Acrescentar seleção explícita de datas na coleta, mantendo uma única localidade e exatamente 30 dias consecutivos. A versão entregue usa o recorte fixo de 01 a 30/10/2026.

Critério de conclusão: O comando deve rejeitar intervalos diferentes de 30 dias e registrar o novo recorte nos metadados, sem substituir o conjunto entregue sem confirmação.

## [#2 - Comparar versões preservadas do JSON](https://github.com/danielperaccini-creator/observatorio-climatico-marilia/issues/2)

Criar uma consulta simples aos arquivos em dados/originais/historico para identificar revisões da fonte em coletas repetidas.

Critério de conclusão: Informar quais datas e variáveis mudaram entre duas respostas, mantendo ambos os JSONs originais e seus hashes.

## [#3 - Mostrar a qualidade dos dados no painel](https://github.com/danielperaccini-creator/observatorio-climatico-marilia/issues/3)

Adicionar ao painel uma seção com a cobertura por variável, ausências e instante da coleta, usando os registros já produzidos pelo tratamento.

Critério de conclusão: Exibir cobertura de 30/30 ou a contagem incompleta, distinguir NULL de zero e manter indisponíveis os indicadores incompletos.

## [#4 - Conferir a reprodução em outro computador](https://github.com/danielperaccini-creator/observatorio-climatico-marilia/issues/4)

Executar o README em um ambiente independente antes da próxima versão e registrar problemas de instalação ou caminho.

Critério de conclusão: Gerar 30 linhas a partir do JSON entregue, repetir a carga sem duplicação e obter os mesmos três indicadores; documentar o ambiente realmente utilizado.

## [#5 - Validar perguntas e explicações com o público](https://github.com/danielperaccini-creator/observatorio-climatico-marilia/issues/5)

Confirmar com moradores que organizam atividades ao ar livre se as três perguntas ajudam a entender o período. A necessidade é proposta e ainda não foi validada em campo.

Critério de conclusão: Registrar uma síntese anônima das dúvidas e decidir, com justificativa, se os indicadores ou suas descrições precisam de ajustes.

## [#6 - Avaliar leitura do dashboard em celular](https://github.com/danielperaccini-creator/observatorio-climatico-marilia/issues/6)

Testar a visualização dos três indicadores, dois gráficos e da tabela em tela pequena, ajustando rótulos e organização quando necessário.

Critério de conclusão: Manter fonte, unidades, período e limitações legíveis sem perda dos indicadores; registrar os ajustes efetivamente feitos.

## [#7 - Realizar e registrar a devolutiva extensionista](https://github.com/danielperaccini-creator/observatorio-climatico-marilia/issues/7)

Preparar a apresentação do painel e explicar extremos, precipitação acumulada, natureza da reanálise e diferença entre histórico e previsão.

Critério de conclusão: Registrar data, público sem identificação individual, atividade, dúvidas, feedback e ajustes. Usar foto ou fala identificável somente com autorização; não registrar a atividade como concluída antes de realizá-la.
