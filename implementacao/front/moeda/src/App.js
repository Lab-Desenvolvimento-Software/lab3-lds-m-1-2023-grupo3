import React, { useState, useEffect } from "react";
import Tabs from "./components/Tabs";

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/aluno/4")
      .then((response) => response.json())
      .then((data) => setData(data));
  }, []);

  if (!data) {
    return <p>Carregando...</p>;
  }

  const {
    aluno, instituicao, transacoes_recebidas, transacoes_enviadas, professores, produtos} = data;
  const tabs = [
    {title: "Tab 1",
     content: (
        <p>
          <h2>Transações Recebidas</h2>
          {transacoes_recebidas.map((transacao) => (
            <div key={transacao.id}>
              <p>ID: {transacao.id}</p>
              <p>Valor: {transacao.valor ?? "N/A"}</p>
              {/* Exiba os demais dados da transação */}
            </div>
          ))}
        </p>)},
    {title: "Tab 2",
     content: (
        <p>
          <h2>Transações Enviadas</h2>
          {transacoes_enviadas.map((transacao) => (
            <div key={transacao.id}>
              <p>ID: {transacao.id}</p>
              <p>Valor: {transacao.valor ?? "N/A"}</p>
              {/* Exiba os demais dados da transação */}
            </div>
          ))}
        </p>)},
    {title: "Tab 3",
     content: (
        <p>
          <h2>Produtos</h2>
          {produtos.map((produto) => (
            <div key={produto.id}>
              <p>ID: {produto.id}</p>
              <p>Nome: {produto.nome ?? "N/A"}</p>
              {/* Exiba os demais dados do produto */}
            </div>
          ))}
        </p>)},
  ];

  return (
    <div className="app">
      <div class="sidebar">
        <h2>Aluno</h2>
        <p>ID: {aluno.id}</p>
        <p>Nome: {aluno.nome}</p>
        <p>Endereço: {aluno.endereco}</p>
        <p>Email: {aluno.email}</p>
        <p>CPF: {aluno.cpf}</p>
        <p>RG: {aluno.rg}</p>
        <p>Instituição: {instituicao.nome}</p>
        <p>moedas: {aluno.moedas}</p>
      </div>

      <div>
        <Tabs tabs={tabs} />
      </div>

      {/* <h2>Professores</h2>
      {professores.map(professor => (
        <div key={professor.id}>
          <p>ID: {professor.id}</p>
          <p>Nome: {professor.nome ?? 'N/A'}</p>
        </div>
      ))} */}
    </div>
  );
}

export default App;
