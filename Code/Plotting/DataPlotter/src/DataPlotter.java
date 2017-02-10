import javax.swing.*;
import java.awt.*;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 */
public class DataPlotter extends Canvas
{
    public static final int WIDTH = 800;
    public static final int HEIGHT = 800;

    public List<LangMatrix> matrices = new ArrayList<>();
    public Rectangle drawSpace = null;

    @Override
    public void paint(Graphics g)
    {
        Rectangle draw = drawSpace != null
                         ? drawSpace
                         : new Rectangle(0, 0, WIDTH, HEIGHT);


        int matrixNum = 22;
        if (matrices != null && matrices.size() > 0)
            matrices.get(matrixNum).render(this, draw);

        System.out.println("Rendering matrix for:  " + matrices.get(matrixNum).getLanguage());

    }

    public static void main(String[] args)
    {
        // Checks for the correct number of arguments
        if (args.length != 1)
        {
            System.out.println("Invalid number of arguments." + "\n" +
                               "Form of the command should be:\n" +
                               "java -jar <JAR NAME> <input path>");
            return;
        }

        // Extract relevant arguments
        String input = args[0];


        DataPlotter dataPlotter = new DataPlotter();


        try (BufferedReader br = new BufferedReader(new FileReader(new File(input))))
        {
            String line;
            String lang = null;
            List<String> data = new ArrayList<>();
            while ((line = br.readLine()) != null)
            {
                if (line.length() == 0)
                    continue;

                if (line.startsWith("#"))
                {
                    if (lang != null)
                        dataPlotter.matrices.add(LangMatrix.build(lang, data));

                    lang = line.substring(1).trim().toLowerCase();
                    data = new ArrayList<>();
                }
                else
                    data.add(line);

            }

            dataPlotter.matrices.add(LangMatrix.build(lang, data));

        } catch (IOException e)
        {
            System.out.println("Error reading input file.");
            return;
        }


        JFrame frame = new JFrame();

        Dimension preferredSize = new Dimension(WIDTH, HEIGHT);
        frame.setPreferredSize(preferredSize);
        frame.pack();
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);

        dataPlotter.setBackground(Color.black);
        dataPlotter.setSize(preferredSize);

        Insets insets = frame.getInsets();
        dataPlotter.drawSpace = new Rectangle(0,
                                              0,
                                              frame.getWidth() - insets.left - insets.right,
                                              frame.getHeight() - insets.top - insets.bottom);

        frame.add(dataPlotter);


    }
}
