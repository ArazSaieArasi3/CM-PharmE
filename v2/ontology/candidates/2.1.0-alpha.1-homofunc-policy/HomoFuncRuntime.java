import RefOntoUML.parser.OntoUMLParser;
import br.ufes.inf.nemo.antipattern.homofunc.HomoFuncAntipattern;

/** Runs the pinned archived class unchanged; no source-policy filtering. */
public class HomoFuncRuntime {
    public static void main(String[] args) throws Exception {
        OntoUMLParser parser = new OntoUMLParser(args[0]);
        HomoFuncAntipattern detector = new HomoFuncAntipattern(parser);
        System.out.println("CMPE_HOMOFUNC_COUNT=" + detector.identify().size());
    }
}
