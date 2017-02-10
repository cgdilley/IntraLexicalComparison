import java.awt.*;
import java.awt.image.BufferedImage;
import java.awt.image.ConvolveOp;
import java.awt.image.Kernel;
import java.awt.image.WritableRaster;
import java.util.ArrayList;
import java.util.List;

/**
 */
public class LangMatrix
{
    public static final Kernel BLUR_KERNEL = buildKernel(10, 3.5);
    public static final double PERCENT_POWER = 2.5;

    private final String language;

    private final List<List<Double>> wordValues;
    private double maxValue = Double.MIN_VALUE;


    /**
     * Private constructor, use static constructor instead.
     */
    private LangMatrix(String language)
    {
        this.language = language;
        this.wordValues = new ArrayList<>();
    }

    /**
     * Static constructor, creates a new language matrix object and returns it.
     *
     * @return The newly constructed LangMatrix object.
     */
    public static LangMatrix build(String language, List<String> data)
    {
        LangMatrix lm = new LangMatrix(language);

        for (int r = 0; r < data.size(); r++)
        {
            String datum = data.get(r);

            String[] tabSplit = datum.split("\t");
            String word = tabSplit[0].split("=")[0];

            List<Double> row = new ArrayList<>();
            String[] values = tabSplit[1].split(" ");
            for (int c = 0; c < values.length; c++)
            {
                String value = values[c];

                double val = Double.parseDouble(value);
                if (val > lm.maxValue && r != c)
                    lm.maxValue = val;
                row.add(val);
            }

            lm.wordValues.add(row);
        }

        for (List<Double> row : lm.wordValues)
            if (row.size() != lm.wordValues.size())
                System.out.println("Mismatched size in " + language);

        return lm;
    }

    public String getLanguage()
    {
        return language;
    }

    public void render(Canvas canvas, Rectangle drawSpace)
    {


        double cW = drawSpace.getWidth() / wordValues.size();
        double cH = drawSpace.getHeight() / wordValues.size();

        BufferedImage output = new BufferedImage(drawSpace.width, drawSpace.height, BufferedImage.TYPE_INT_RGB);

        Graphics g = output.getGraphics();


        for (int x = 0; x < wordValues.size(); x++)
        {
            for (int y = 0; y < wordValues.size(); y++)
            {
                g.setColor(new Color(getColorOfPercent(wordValues.get(y).get(x) / maxValue)));
                g.fillRect((int)(x * cW) + drawSpace.x,
                           (int)(y * cH) + drawSpace.y,
                           (int)Math.ceil(cW), (int)Math.ceil(cH));
            }
        }

        // Blur the image
        ConvolveOp op = new ConvolveOp(BLUR_KERNEL );
        WritableRaster raster = output.getRaster();
        output.setData(op.filter(raster, op.createCompatibleDestRaster(raster)));

        canvas.getGraphics().drawImage(output, 0, 0, null);

    }

    public int getColorOfPercent(double percent)
    {
        if (percent > 1)
            percent = 1;

        percent = Math.pow(percent, PERCENT_POWER);

        Color[] colorSeq = {Color.green, Color.black};
        double[] colorPos = {0, 1};
        
        int r = colorSeq[0].getRed(), g = colorSeq[0].getGreen(), b = colorSeq[0].getBlue();
        for (int i = 0; i < colorPos.length - 1; i++)
        {
            if (!(colorPos[i] < percent && colorPos[i+1] > percent))
                continue;
            
            double percDist = colorPos[i+1] - colorPos[i];
            double weight1 = (percent - colorPos[i]) / percDist;
            double weight2 = (colorPos[i+1] - percent) / percDist;
            
            r = (int)((colorSeq[i].getRed() * weight1) + (colorSeq[i+1].getRed() * weight2));
            g = (int)((colorSeq[i].getGreen() * weight1) + (colorSeq[i+1].getGreen() * weight2));
            b = (int)((colorSeq[i].getBlue() * weight1) + (colorSeq[i+1].getBlue() * weight2));
            
            break;
        }


        return r << 16 | g << 8 | b;
    }

    private static Kernel buildKernel(int size, double sharpness)
    {
        if (size%2 == 0)
            size++;

        float[] kernel = new float[size*size];

        int radius = size/2;

        double totalWeight = 0;
        for (int x = 0; x < size; x++)
        {
            for (int y = 0; y < size; y++)
            {
                int manhatDist = Math.abs(radius - x) + Math.abs(radius - y);
                int exponent = (radius + 1) - manhatDist;
                double factor = Math.pow(sharpness, exponent);

                kernel[x + (y * size)] = (float)factor;

                totalWeight += factor;
            }
        }

        for (int i=0; i<kernel.length; i++)
            kernel[i] /= totalWeight;

        return new Kernel(size, size, kernel);
    }

}
