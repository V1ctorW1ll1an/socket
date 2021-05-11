const net = require("net");
const prompt = require("prompt-sync")();
const dgram = require("dgram");

const host = "public ip here";
const port_tcp = 65432;
const port_udp = 65431;
const timeout = 15000;

function back_to_menu() {
  prompt("\n\nAperte <Enter> para continuar\n\n");
  menu();
}

function date_format(parameter) {
  try {
    let is_valid_date = /[12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])/.test(
      parameter
    );
    if (!is_valid_date) {
      console.log(
        "\nA data informada está no formato incorreto tente o ex: 2020-02-10"
      );
      back_to_menu();
    } else {
      let new_date = new Date(parameter);
      let month = new_date.getUTCMonth() + 1; //meses de 1-12
      let day = new_date.getUTCDate();
      let year = new_date.getUTCFullYear();

      return month < 10
        ? day < 10
          ? `${year}0${month}0${day}`
          : `${year}0${month}${day}`
        : day < 10
        ? `${year}${month}0${day}`
        : `${year}${month}${day}`;
    }
  } catch (error) {
    console.log(
      "Ocorreu um erro ao converter a data, verifique se está no formato correto  ex: 2020-02-10"
    );
    back_to_menu();
  }
}

function start_connection(method, parameter) {
  try {
    const client = net.connect(port_tcp, host, () => {
      const my_json = JSON.stringify({
        method: method,
        parameter: parameter,
      });
      client.write(my_json);
    });
    client.on("data", (data) => {
      data_str = JSON.parse(data.toString());
      console.log("\n");
      if ("msg" in data_str) {
        console.log(`\n${data_str["msg"]}`);
      } else {
        console.table(data_str);
      }
      client.end();
    });
    client.on("error", () => {
      console.log(
        "\nNão foi possível estabelecer uma conexão com o servidor!\n"
      );
      back_to_menu();
    });
    client.on("end", () => {
      back_to_menu();
    });
    client.setTimeout(timeout, () => {
      console.log("\nA tentativa de conexão excedeu o valor limite de tempo\n");
      client.destroy();
      back_to_menu();
    });
    client.once("connect", () => client.setTimeout(0));
  } catch (error) {
    console.log(
      "\n\nOcorreu um erro inesperado ao tentar se conectar com o servidor: ",
      error,
      "\n\n"
    );
    back_to_menu();
  }
}

function start_udp_connection(method, parameter) {
  try {
    const udp_client = dgram.createSocket("udp4");

    const id = setTimeout(() => {
      clearTimeout(id);
      udp_client.close();
      console.log("\nA tentativa de conexão excedeu o valor limite de tempo\n");
      back_to_menu();
    }, parseInt(timeout));

    udp_client.send(
      JSON.stringify({
        method: method,
        parameter: parameter,
      }),
      port_udp,
      host,
      (err) => {
        if (err) {
          clearTimeout(id);
          console.log(err);
          back_to_menu();
        }
      }
    );

    udp_client.on("error", (err) => {
      clearTimeout(id);
      console.log(`udp_client error:\n${err.stack}`);
      udp_client.close();
    });

    udp_client.on("message", (data, rinfo) => {
      clearTimeout(id);
      data_str = JSON.parse(data.toString());
      if ("msg" in data_str) {
        console.log(`\n${data_str["msg"]}`);
      } else {
        console.table(data_str);
      }
      back_to_menu();
    });
  } catch (error) {
    console.log(error);
    back_to_menu();
  }
}

function menu() {
  try {
    process.stdout.write("\033c");
    console.log("\n\n BEM VINDO\n\n");
    console.log("ESCOLHA UMA OPÇÃO DE BUSCA \n\n");
    console.log("1 - Pesquisar dados pela UF (UFs brasileiras)\n");
    console.log("2 - Pesquisar dados pela data\n");
    console.log(
      "3 - Pesquisar dados pelo pais (brazil) utilizando o protocolo TCP\n"
    );
    console.log(
      "4 - Pesquisar dados pelo pais (brazil) utilizando o protocolo UDP\n"
    );
    console.log("5 - Sair do programa\n");

    let option = prompt("opção: => ");
    console.log("\n\n");

    if (!option || ![1, 2, 3, 4, 5].includes(+option)) {
      console.log("Por favor, insira uma opção válida!");
      back_to_menu();
    }

    let method;
    let parameter;
    switch (+option) {
      case 1:
        method = "pesquisar_dados_por_uf";
        parameter = prompt("Informe a uf: => ");
        start_connection(method, parameter);
        break;
      case 2:
        method = "pesquisar_dados_por_data";
        parameter = prompt("Informe a data (ano-mes-dia) ex: 2020-02-25: => ");
        parameter = date_format(parameter);
        start_connection(method, parameter);
        break;
      case 3:
        method = "pesquisar_dados_por_pais";
        console.log(
          "Obs: Não abrange todos os países do mundo, apenas alguns como (Germany, Brazil, Canada, Argentina, Bolivia, Spain)\n\n"
        );
        parameter = prompt("Informe o pais => ");
        start_connection(method, parameter || "brazil");
        break;
      case 4:
        method = "pesquisar_dados_por_pais";
        console.log(
          "Obs: Não abrange todos os países do mundo, apenas alguns como (Germany, Brazil, Canada, Argentina, Bolivia, Spain)\n\n"
        );
        parameter = prompt("Informe o pais => ");
        start_udp_connection(method, parameter || "brazil");
        break;
      case 5:
        process.exit(1);
      default:
        break;
    }
  } catch (error) {
    console.log(
      "\n\nOcorreu um erro ao executar a função do menu: ",
      error,
      "\n\n"
    );
    back_to_menu();
  }
}

(function main() {
  menu();
})();
