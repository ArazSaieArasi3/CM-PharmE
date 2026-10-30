import RefOntoUML.parser.OntoUMLParser;
import br.ufes.inf.nemo.antipattern.relcomp.RelCompAntipattern;

/** Runs the pinned archived class unchanged; no source-policy filtering. */
public class RelCompRuntime {
    public static void main(String[] args) throws Exception {
        OntoUMLParser parser = new OntoUMLParser(args[0]);
        RelCompAntipattern detector = new RelCompAntipattern(parser);
        System.out.println("CMPE_RELCOMP_COUNT=" + detector.identify().size());
    }
}
