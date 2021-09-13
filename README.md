# desktop-chrome-background

Mantém o background do chrome igual ao do desktop.
Feito para o Ubuntu.

## Modo de uso

Usado junto com incron: https://www.linux.com/topic/desktop/how-use-incron-monitor-important-files-and-folders/

### Instalação:

    $ sudo apt install incron

### As configurações são:

Executar:

    $ nano /etc/incron.allow

Adicionar:

    root
    user

Trocar user pelo nome de seu usuário.

Executar:
    
    $ incrontab -e

Adicionar:

    /home/vitor/.config/dconf/user  IN_MODIFY       python3 /home/vitor/my-daemons/desktop-chrome-background/main.py

Clonar o repositório para /home/vitor/my-daemons/desktop-chrome-background/ de modo que main.py possa ser acessado como /home/vitor/my-daemons/desktop-chrome-background/main.py