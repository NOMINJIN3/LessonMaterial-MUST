import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.*;
import java.io.*;

public class CitizenGUI extends JFrame {
    private CitizenRegistry registry = new CitizenRegistry();
    private JTextArea outputArea;

    public CitizenGUI() {
        setTitle("Иргэний бүртгэлийн систем");
        setSize(600, 400);
        setDefaultCloseOperation(EXIT_ON_CLOSE);

        JButton loadButton = new JButton("Өгөгдөл ачаалах");
        JButton saveButton = new JButton("Өгөгдөл хадгалах");
        JButton addButton = new JButton("Шинэ иргэн нэмэх");
        JButton searchButton = new JButton("РД-р хайх");

        outputArea = new JTextArea();
        outputArea.setEditable(false);

        loadButton.addActionListener(e -> loadCitizens());
        saveButton.addActionListener(e -> saveCitizens());
        addButton.addActionListener(e -> addCitizen());
        searchButton.addActionListener(e -> searchCitizen());

        JPanel panel = new JPanel();
        panel.add(loadButton);
        panel.add(saveButton);
        panel.add(addButton);
        panel.add(searchButton);

        add(panel, BorderLayout.NORTH);
        add(new JScrollPane(outputArea), BorderLayout.CENTER);
    }

    private void loadCitizens() {
        try {
            List<Citizen> citizens = FileManager.readCitizens("citizens.txt");
            for (Citizen c : citizens) {
                registry.addCitizen(c);
                outputArea.append(c.toString() + "\n");
            }
        } catch (IOException ex) {
            JOptionPane.showMessageDialog(this, "Файл уншихад алдаа гарлаа.");
        }
    }

    private void saveCitizens() {
        try {
            FileManager.writeCitizens("citizens.txt", registry.getAllCitizens());
            JOptionPane.showMessageDialog(this, "Амжилттай хадгалагдлаа.");
        } catch (IOException ex) {
            JOptionPane.showMessageDialog(this, "Файл бичихэд алдаа гарлаа.");
        }
    }

    private void addCitizen() {
        try {
            String name = JOptionPane.showInputDialog("Нэр:");
            String id = JOptionPane.showInputDialog("РД:");
            String birth = JOptionPane.showInputDialog("Төрсөн огноо:");
            String gender = JOptionPane.showInputDialog("Хүйс:");
            String province = JOptionPane.showInputDialog("Аймаг/Хот:");
            String district = JOptionPane.showInputDialog("Сум/Дүүрэг:");
            String street = JOptionPane.showInputDialog("Гудамж/Баг:");

            if (name != null && id != null && birth != null && gender != null && province != null && district != null
                    && street != null) {
                Address addr = new Address(province, district, street);
                Citizen c = new Citizen(name, id, birth, gender, addr);
                registry.addCitizen(c);
                outputArea.append(c.toString() + "\n");
            }
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "Өгөгдөл нэмэхэд алдаа гарлаа.");
        }
    }

    private void searchCitizen() {
        try {
            String id = JOptionPane.showInputDialog("Хайх РД оруулна уу:");
            List<Citizen> result = registry.searchById(id);
            outputArea.setText("");
            for (Citizen c : result) {
                outputArea.append(c.toString() + "\n");
            }
            if (result.isEmpty()) {
                outputArea.setText("Иргэн олдсонгүй.");
            }
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "Хайлт хийхэд алдаа гарлаа.");
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new CitizenGUI().setVisible(true));
    }
}
