import psycopg2
from dataclasses import dataclass

@dataclass
class Banco:
    nome: str
    senha: str
    usuario: str
    ip: str
    porta: str
    conexao: psycopg2.extensions.connection = None

    @property
    def connect(self) -> None:
        try:
            self.conexao = psycopg2.connect(
                f"host='{self.ip}' "\
                f"user='{self.usuario}' "\
                f"password='{self.senha}' "\
                f"dbname='{self.nome}' "\
                f"port={self.porta}"
            )
            print("\033[1;32mConexão realizada com sucesso!\033[0m")
        except psycopg2.OperationalError as e:
            print("\033[1;31mErro ao conectar:", e, "\033[0m")

    
    def insert(self, nome: str, colunas: tuple, valores: tuple) -> None:
        self.connect
        cursor = self.conexao.cursor()

        insert_script = f"""INSERT INTO tabnet.{nome} ({', '.join(['"'+c+'"' for c in colunas])}) VALUES ({', '.join(['%s']*len(colunas))})"""
        
        cursor.execute(insert_script, valores)

        print("\033[1;30;42mDado inserido com sucesso!\033[0m")
        
        self.conexao.commit()
        cursor.close()
        self.conexao.close()

    
    def verify_data(self, nome: str, hash: str) -> bool:
        self.connect
        cursor = self.conexao.cursor()

        verify_script = f"SELECT hash FROM tabnet.{nome} WHERE hash = '{hash}'"
        cursor.execute(verify_script)
        resultado = cursor.fetchall()
        
        cursor.close()
        self.conexao.close()
        self.conexao = None
        
        return len(resultado) != 0