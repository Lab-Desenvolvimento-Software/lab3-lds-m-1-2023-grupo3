// const [data, setData] = useState(null);
import React, { useState, useEffect } from "react";
import axios from "axios";
import Tabs from "./Tabs";

function Aluno() {
  const [alunoData, setAlunoData] = useState(null);
  const [transacoesData, setTransacoesData] = useState(null);

  useEffect(() => {
    fetchAlunoData();
    fetchTransacoesData();
  }, []);

  const fetchAlunoData = () => {
    axios.get("http://127.0.0.1:5000/aluno/4")
      .then((response) => {
        setAlunoData(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const fetchTransacoesData = () => {
    axios.get("http://127.0.0.1:5000/transacoes/4")
      .then((response) => {
        setTransacoesData(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const compraProduto = (produtoId) => {
    axios.post(`http://127.0.0.1:5000/aluno/4/compra/${produtoId}`)
      .then((response) => {
        console.log(response.data);
        // Atualize os dados do aluno e das transações após a compra ser realizada
        fetchAlunoData();
        fetchTransacoesData();
      })
      .catch((error) => {
        console.log(error);
      });
  };


  if (!transacoesData || !alunoData) {
    return <p>Carregando...</p>;
  }

  const { aluno, instituicao, produtos } = alunoData;
  const { transacoes_recebidas, transacoes_enviadas } = transacoesData;
  const tabs = [
    {
      title: "Transações recebidas",
      content: (
        <p>
          <h2>Transações Recebidas</h2>
          {transacoes_recebidas.map((transacao) => (
            <div class="transacao" key={transacao.id}>
              <p>Origem: {transacao.tipo} {transacao.origem}</p>
              <p>Valor: {transacao.valor}</p>
              <p>Mensagem: {transacao.mensagem}</p>
              <p>Data: {transacao.data}</p>
            </div>
          ))}
        </p>)
    },
    {
      title: "Transações enviadas",
      content: (
        <p>
          <h2>Transações Enviadas</h2>
          {transacoes_enviadas.map((transacao) => (
            <div key={transacao.id}>
              <p>destino: {transacao.destino}</p>
              <p>Valor: {transacao.valor}</p>
              <p>Mensagem: {transacao.mensagem}</p>
              <p>Data: {transacao.data}</p>
            </div>
          ))}
        </p>)
    },
    {
      title: "Produtos",
      content: (
        <p>
          <h2>Produtos</h2>
          {produtos.map((produto) => (
            <div key={produto.id}>
              <p>ID: {produto.id}</p>
              <p>Nome: {produto.nome}</p>
              <button onClick={() => compraProduto(produto.id)}>Comprar</button>
            </div>
          ))}
        </p>)
    },
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

export default Aluno;