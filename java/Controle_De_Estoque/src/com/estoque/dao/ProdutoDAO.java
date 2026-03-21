package com.estoque.dao;

import com.estoque.model.Produto;
import com.estoque.model.Categoria;
import com.estoque.config.ConnectionFactory;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class ProdutoDAO {

    // CREATE
    public void inserir(Produto produto) throws SQLException {
        String sql = "INSERT INTO produtos (nome, quantidade, preco, categoria_id) VALUES (?, ?, ?, ?)";

        try (Connection conn = ConnectionFactory.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setString(1, produto.getNome());
            stmt.setInt(2, produto.getQuantidade());
            stmt.setDouble(3, produto.getPreco());
            stmt.setInt(4, produto.getCategoria().getId());

            stmt.executeUpdate();
        }
    }

    // READ
    public List<Produto> listar() throws SQLException {
        List<Produto> lista = new ArrayList<>();

        String sql = """
            SELECT p.*, c.nome AS categoria_nome
            FROM produtos p
            JOIN categorias c ON p.categoria_id = c.id
        """;

        try (Connection conn = ConnectionFactory.getConnection();
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {

            while (rs.next()) {
                Produto p = new Produto();
                p.setId(rs.getInt("id"));
                p.setNome(rs.getString("nome"));
                p.setQuantidade(rs.getInt("quantidade"));
                p.setPreco(rs.getDouble("preco"));

                Categoria c = new Categoria();
                c.setId(rs.getInt("categoria_id"));
                c.setNome(rs.getString("categoria_nome"));

                p.setCategoria(c);

                lista.add(p);
            }
        }

        return lista;
    }

    // UPDATE
    public void atualizar(Produto produto) throws SQLException {
        String sql = """
            UPDATE produtos 
            SET nome = ?, quantidade = ?, preco = ?, categoria_id = ?
            WHERE id = ?
        """;

        try (Connection conn = ConnectionFactory.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setString(1, produto.getNome());
            stmt.setInt(2, produto.getQuantidade());
            stmt.setDouble(3, produto.getPreco());
            stmt.setInt(4, produto.getCategoria().getId());
            stmt.setInt(5, produto.getId());

            stmt.executeUpdate();
        }
    }

    // UPDATE específico (estoque)
    public void atualizarQuantidade(int id, int quantidade) throws SQLException {
        String sql = "UPDATE produtos SET quantidade = ? WHERE id = ?";

        try (Connection conn = ConnectionFactory.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setInt(1, quantidade);
            stmt.setInt(2, id);
            stmt.executeUpdate();
        }
    }

    // DELETE
    public void deletar(int id) throws SQLException {
        String sql = "DELETE FROM produtos WHERE id = ?";

        try (Connection conn = ConnectionFactory.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setInt(1, id);
            stmt.executeUpdate();
        }
    }
}
