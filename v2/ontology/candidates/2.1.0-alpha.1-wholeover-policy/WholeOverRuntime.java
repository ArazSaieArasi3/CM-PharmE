import RefOntoUML.parser.OntoUMLParser;
import br.ufes.inf.nemo.antipattern.wholeover.WholeOverAntipattern;

/** Runs the pinned archived class unchanged; no source-policy filtering. */
public class WholeOverRuntime {
    public static void main(String[] args) throws Exception {
        OntoUMLParser parser = new OntoUMLParser(args[0]);
        WholeOverAntipattern detector = new WholeOverAntipattern(parser);
        System.out.println("CMPE_WHOLEOVER_COUNT=" + detector.identify().size());
    }
}
