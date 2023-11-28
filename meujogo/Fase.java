package meujogo;

import javax.swing.JPanel;

import javax.swing.ImageIcon;

import java.awt.Image;
import java.awt.Graphics;
import java.awt.Graphics2D;

public class Fase extends JPanel {
    
    private Image fundo;

    public Fase() {
        ImageIcon referencia = new ImageIcon("assets\\screens\\StartScreen.png");
        
        fundo = referencia.getImage();
        System.out.println("aqui");
    }

    public void paint (Graphics g) {
        Graphics2D graficos = (Graphics2D) g;
        graficos.drawImage(fundo, 0, 0, null);
        g.dispose();
    }

}
