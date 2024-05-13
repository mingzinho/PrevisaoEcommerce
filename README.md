Antes de clonar o repositorio certifique-se de ter o Build Tools e o Cx_Oracle baixados no seu computador, para poder realizar a conexão com o banco de dados.

Build Tools:
https://visualstudio.microsoft.com/pt-br/visual-cpp-build-tools/

Baixe a versão mais recente do basic packagem em:
https://www.oracle.com/database/technologies/instant-client/winx64-64-downloads.html

Após isso extraia e copie o diretorio da pasta, substituindo na linha 12 codigo o caminho.



Após clonar o repositorio utilize os seguintes comandos:

1 - "python -m pip install --upgrade --force-reinstall pip" para reinstalar o Python e utilizar diretamente o do seu computador.

2 - "pip install -r  requirements.txt" para baixar os packages necessarios.

3 - "python -m streamlit run teste.py" para rodar a aplicação



