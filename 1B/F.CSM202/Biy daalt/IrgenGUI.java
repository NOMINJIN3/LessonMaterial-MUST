
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class IrgenGUI extends JFrame {
    private JTextField nameField, idField, birthField, genderField, provinceField, districtField, streetField;
    private JTextArea outputArea;

    public IrgenGUI() {
        setTitle("Irgenii GUI system");
        setSize(500, 400);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

     
        JPanel inputPanel = new JPanel(new GridLayout(7, 2));
        inputPanel.add(new JLabel("Ner:"));
        nameField = new JTextField();
        inputPanel.add(nameField);

        inputPanel.add(new JLabel("Registeriin dugaar:"));
        idField = new JTextField();
        inputPanel.add(idField);

        inputPanel.add(new JLabel("Tursun udur:"));
        birthField = new JTextField();
        inputPanel.add(birthField);

        inputPanel.add(new JLabel("Huis:"));
        genderField = new JTextField();
        inputPanel.add(genderField);

        inputPanel.add(new JLabel("Aimag/Hot:"));
        provinceField = new JTextField();
        inputPanel.add(provinceField);

        inputPanel.add(new JLabel("Sum/Duureg:"));
        districtField = new JTextField();
        inputPanel.add(districtField);

        inputPanel.add(new JLabel("Gudamj/Bag:"));
        streetField = new JTextField();
        inputPanel.add(streetField);

      
        outputArea = new JTextArea();
        outputArea.setEditable(false);

        JButton addButton = new JButton("Burtgeh");
        addButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                String ner = nameField.getText();
                String rd = idField.getText();
                String tursun = birthField.getText();
                String huis = genderField.getText();
                String aimag = provinceField.getText();
                String duureg = districtField.getText();
                String gudamj = streetField.getText();

                String result = "Ner: " + ner + "\nRegisteriin dugaar: " + rd + "\nTursunudur: " + tursun +
                        "\nHuis: " + huis + "\nHayag: " + aimag + ", " + duureg + ", " + gudamj + "\n\n";

                outputArea.append(result);
                clearFields();
            }
        });

        add(inputPanel, BorderLayout.NORTH);
        add(addButton, BorderLayout.CENTER);
        add(new JScrollPane(outputArea), BorderLayout.SOUTH);
    }

    private void clearFields() {
        nameField.setText("");
        idField.setText("");
        birthField.setText("");
        genderField.setText("");
        provinceField.setText("");
        districtField.setText("");
        streetField.setText("");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            new IrgenGUI().setVisible(true);
        });
    }
}
