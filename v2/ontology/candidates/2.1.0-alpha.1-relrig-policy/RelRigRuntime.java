import RefOntoUML.parser.OntoUMLParser;
import br.ufes.inf.nemo.antipattern.relrig.RelRigAntipattern;

/** Runs the pinned archived class unchanged; no source-policy filtering. */
public class RelRigRuntime {
    public static void main(String[] args) throws Exception {
        OntoUMLParser parser = new OntoUMLParser(args[0]);
        RelRigAntipattern detector = new RelRigAntipattern(parser);
        System.out.println("CMPE_RELRIG_COUNT=" + detector.identify().size());
    }
}
