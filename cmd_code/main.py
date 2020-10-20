import os
import configparser
from argparse import ArgumentParser
from gooey import Gooey, GooeyParser

config = configparser.ConfigParser()
config.read('config.ini')

Hmax = config['default']['Hmax']
Hmin = config['default']['Hmin']
Smax = config['default']['Smax']
Smin = config['default']['Smin']
Vmax = config['default']['Vmax']
Vmin = config['default']['Vmin']
Bsize = config['default']['Bsize']
blur = config['default']['blur']
L = config['default']['L']
L_pixel = config['default']['L_pixel']

@Gooey(
    program_name="Tracker++",
    program_description="Processa e identifica objetos para experimentos de cinemática",
    default_size=(600, 480),
    progress_regex=r"^Progress (\d+)$",
    # image_dir='/Users/gustavo/Desktop/pendulo'
)
def main():
    parser = GooeyParser() 
    parser._optionals.title = "Opções"
    parser._optionals.description = f'Comprimento Fio: {L}, L_lixel: {L_pixel}\nFiltro de cor - Max: H={Hmax}, S={Smax}, V={Vmax} \n \t         Min: H={Hmax}, S={Smax}, V={Vmax} \n \t         Blur: {blur} , Bsize"{Bsize}'
    parser.add_argument(
        "-e",
        "--Entrada", 
        required=True,
        help="Arquivo de Vídeo a ser processado",
        widget="FileChooser",
        default=os.getcwd(),
        gooey_options=dict(wildcard="Video files (*.mp4, *.mkv)|*.mp4;*.mkv")
    )
    parser.add_argument(
        "-s",
        "--saida",
        required=True,
        help="Caminho para arquivo de saída",
        widget="FileSaver",
        default=os.getcwd(),
        gooey_options=dict(wildcard="MPEG-4 (.mp4)|*.mp4")
    )
    parser.add_argument(
        "--acao",
        metavar="Ação",
        help="Escolha a ação a ser realizada",
        required=True,
        widget="Dropdown",
        choices=["Processar vídeo", "Ajuste Parâmetros", "Ajuste tamanho"],
        default="Processar vídeo",
    )
    args = parser.parse_args()
    print(args.acao, args.saida, args.acao)

if __name__ == '__main__':
    main()