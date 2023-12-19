///Ethiet,h150714@stud.u-szeged.hu
import java.util.*;
import game.racetrack.Direction;
import game.racetrack.RaceTrackGame;
import game.racetrack.RaceTrackPlayer;
import game.racetrack.utils.Cell;
import game.racetrack.utils.Coin;
import game.racetrack.utils.PlayerState;

/**
 * Az ágens osztálya, amely egy speciális RaceTrackPlayer
 */
public class Agent extends RaceTrackPlayer {

    /** A pálya mezői */
    private final SearchCell[][] trackCells;
    /** Az ágens által végrehajtott akciók listája */
    private List<Direction> actions;
    /** Az aktuális akció indexe */
    private int actionIndex = 0;
    /** A célként kiválasztott mező i koordinátája */
    private final int finishI;
    /** A célként kiválasztott mező j koordinátája */
    private final int finishJ;
    /** A négy szomszédos irány */
    private Direction[] fourWayNeighbours = new Direction[] {
            new Direction(1,0),
            new Direction(0,1),
            new Direction(-1,0),
            new Direction(0,-1)
    };
    List<Coin> coinList;

    /**
     * Az osztály kosnstruktora, inicializálja az ágenst
     * @param state Az ágens kezdeti állapota
     * @param random Egy előre megadott random, beállított seed-del (minden random hívás ezt használja, ha van)
     * @param track A pályát leíró 2D tömb
     * @param coins A pályán lévő coinok
     * @param color Az ágens színe
     */
    public Agent(PlayerState state, Random random, int[][] track, Coin[] coins, int color) {
        super(state, random, track, coins, color);

        coinList =  new ArrayList<>(Arrays.asList(coins));

        finishI = 0;
        finishJ = track[0].length-6;

        trackCells = new SearchCell[track.length][track[0].length];
        init();
    }

    /**
     * Speciális cella, amely extra funkciókkal rendelkezik
     */
    private static class SearchCell extends Cell{
        /** Az elérési költség */
        public double reachCost = Double.MAX_VALUE;
        /** A teljes költség */
        public double totalCost = Double.MAX_VALUE;
        /** A heurisztika értéke*/
        public double heuristics;
        /** A szülője */
        public SearchCell parent = null;
        /** a rálépés költsége */
        public int stepCost = 1;
        /** van-e rajta coin */
        public boolean hasCoin = false;
        public Coin closeCoin = null;
        /** az adott mezőn lévő aktuális sebesség */
        public Velocity velocity = new Velocity(0, 0);

        /**
         * Létrehoz egy cellát, amelyet kersesésnél használhatunk.
         *
         * @param i      sor index
         * @param j      oszlop index
         * @param parent szülő objektum
         * @param reachCost az eddig megtett út költsége (elérési költség)
         * @param totalCost az útiköltség és a heurisztika költségének az összege,
         */
        public SearchCell(int i, int j) {
            super(i, j);
        }

        /**
         * készít egy másoltot az objektumból, de beállítja mellé a velocity-t az adott értékre
         * Itt optimalizálható a heurisztika, amennyiben a sebességet is bele akarjuk venni
         * */
        public SearchCell cloneWithNewVelocity(Velocity _velocity){
            SearchCell clone = new SearchCell(i, j);
            clone.reachCost = reachCost;
            clone.heuristics = heuristics;
            clone.closeCoin = closeCoin;
            clone.totalCost = clone.reachCost + clone.heuristics;
            clone.parent = parent;
            clone.stepCost = stepCost;
            clone.hasCoin = hasCoin;
            clone.velocity = _velocity;
            return clone;
        }

        /** megadja hány koordinátája tér el egy másik cellához képest */
        public int cordDiff(SearchCell other){
            if(other == null) return 0;
            return (i != other.i? 1 : 0) + (j != other.j? 1 : 0);
        }
        /** megmondja hogy azonos típusúak és egyező értékűek-e */
        @Override
        public boolean equals(Object obj) {
            if (obj instanceof SearchCell) {
                SearchCell s = (SearchCell) obj;
                return i == s.i && j == s.j && velocity.i == s.velocity.i && velocity.j == s.velocity.j;
            }
            return false;
        }
        /** összehasonlítja egy másik objektummal */
        /**
         * felülírt hashcode, ami az egyezést i, j, velocity.i és velocity.j alapján nézi
         */
        @Override
        public int hashCode(){
            return Objects.hash(i, j, velocity.i, velocity.j);
        }
    }

    /** két SearchCell-t hasonlít össze a teljes költségük alapján */
    private static class SearchCellComparator implements Comparator<SearchCell>{
        /** összehasonlít */
        public int compare(SearchCell s1, SearchCell s2) {
            return (int)Math.round(s1.totalCost - s2.totalCost);
        }
    }

    /** megadja hogy a validak-e a koordináták és nem fal */
    private boolean isValidFreeCell(int i, int j){
        return 0 <= i && i < track.length && 0 <= j && j < track[0].length && track[i][j] != RaceTrackGame.WALL;
    }

    /** Összehasonlítható sebesség osztály, olyan mint a Direction csak lehet nagyobb mint 1 abs értékű coordinátája is */
    private static class Velocity implements Comparable<Velocity> {
        /** i irányú sebesség */
        public int i;
        /** j irányú sebesség */
        public int j;

        /** konstruktor */
        public Velocity(int i, int j) {
            this.i = i;
            this.j = j;
        }

        /** megmondja hogy egyeznek e az i és j sebességek */
        public boolean same(Velocity velocity) {
            return velocity != null && velocity.i == i && velocity.j == j;
        }

        /** megmondja hogy azonos típusúak és egyező értékűek-e */
        @Override
        public boolean equals(Object obj) {
            if (obj instanceof Velocity) {
                Velocity v = (Velocity)obj;
                return same(v);
            }
            return false;
        }

        /** összehasonlítja egy másik objektummal */
        @Override
        public int compareTo(Velocity o) {
            if (i < o.i || (i == o.i && j < o.j)) {
                return -1;
            }
            if (o.i < i || (i == o.i && o.j < j)) {
                return 1;
            }
            return 0;
        }

        /** a legnagyobb abszolútértékű koordinátáját adja vissza */
        public int maxAbs(){
            return Math.max(Math.abs(i), Math.abs(j));
        }

        /** (vi,vj) */
        @Override
        public String toString() {
            return "(" + i + "," + j + ")";
        }
    }

    /** A* algoritmus, amely megtalálja a legrövidebb utat a @param start cellából a legközelebbi coinhoz, vagy a célhoz*/
    public List<SearchCell> aStar(SearchCell start, boolean coinSearch){
        PriorityQueue<SearchCell> open = new PriorityQueue<>(track.length*track[0].length, new SearchCellComparator());
        HashSet<SearchCell> closed = new HashSet<>(track.length*track[0].length);

        open.add(start);

        while(!open.isEmpty()){
            SearchCell current = open.peek();

            if((coinSearch && current.hasCoin && current.velocity.maxAbs() == 0) || ((track[current.i][current.j] & RaceTrackGame.FINISH) == RaceTrackGame.FINISH && !coinSearch)){
                List<SearchCell> result = new ArrayList<>();
                while(current != start.parent){
                    result.add(0, current);
                    current = current.parent;
                }
                return result;
            }else{
                open.remove();
                closed.add(current);

                for(Direction dir: RaceTrackGame.DIRECTIONS){
                    Velocity targetVelocity = new Velocity(current.velocity.i + dir.i, current.velocity.j + dir.j);
                    int targetI = current.i + targetVelocity.i;
                    int targetJ = current.j + targetVelocity.j;

                    if(!isValidFreeCell(targetI, targetJ) || hasWallInTheWay(current.i, current.j, targetI, targetJ)) continue;

                    SearchCell neighbour = trackCells[targetI][targetJ].cloneWithNewVelocity(targetVelocity);

                    if((!open.contains(neighbour) && !closed.contains(neighbour)) || current.reachCost + neighbour.stepCost < neighbour.reachCost){
                        neighbour.reachCost = current.reachCost + neighbour.stepCost;
                        neighbour.velocity = targetVelocity;
                        neighbour.parent = current;
                        neighbour.totalCost = neighbour.reachCost + neighbour.heuristics;
                        open.add(neighbour);
                        closed.remove(neighbour);
                    }
                }
            }
            closed.add(current);
        }
        return null;
    }

    /** megnézi, hogy két cella közt van-e fal */
    private boolean hasWallInTheWay(int currentI, int currentJ, int targetI, int targetJ){
        List<Cell> hitCells = RaceTrackGame.line8connect(new Cell(currentI, currentJ), new Cell(targetI, targetJ));

        for(Cell cell: hitCells){
            if(track[cell.i][cell.j] == RaceTrackGame.WALL) return true;
        }
        return false;
    }

    /** beállítja a heurisztikát a céltól vett távolságra */
    private void updateFinishNeighbours(){
        Set<SearchCell> open = new HashSet<>();
        Set<SearchCell> closed = new HashSet<>();
        int iteration = 1;

        trackCells[finishI][finishJ].heuristics = 0;
        addFourWayNeighbours(trackCells[finishI][finishJ], open, closed);

        while(!open.isEmpty()){
            SearchCell[] iterationCells = open.toArray(new SearchCell[0]);
            open.clear();

            for(SearchCell cell: iterationCells){
                cell.heuristics = iteration;
                cell.hasCoin = false;
                addFourWayNeighbours(cell, open, closed);
            }

            iteration++;
        }
    }

    /** frissíti a coin szomszédjait, hogy a heurisztikájuk legyen a legközelebbi cointól vett távolság*/
    private void updateCoinNeighbours(List<Coin> coinList){
        Set<SearchCell> open = new HashSet<>();
        Set<SearchCell> closed = new HashSet<>();
        int iteration = 1;

        for(Coin coin: coinList){
            trackCells[coin.i][coin.j].heuristics = 0;
            trackCells[coin.i][coin.j].closeCoin = coin;
            trackCells[coin.i][coin.j].hasCoin = true;
            addFourWayNeighbours(trackCells[coin.i][coin.j], open, closed);
        }

        while(!open.isEmpty()){
            SearchCell[] iterationCells = open.toArray(new SearchCell[0]);
            open.clear();

            for(SearchCell cell: iterationCells){
                cell.heuristics = iteration;
                if(cell.parent != null) cell.closeCoin = cell.parent.closeCoin;
                addFourWayNeighbours(cell, open, closed);
            }

            iteration++;
        }
    }

    /** kezeli a nyílt és zárt halmazt, az originből vett 4 szomszédos mezőt beveszi, ha be kell*/
    private void addFourWayNeighbours(SearchCell origin, Set<SearchCell> open, Set<SearchCell> closed){
        closed.add(origin);

        for(Direction dir: fourWayNeighbours){
            int targetI = origin.i + dir.i;
            int targetJ = origin.j + dir.j;
            if(isValidFreeCell(targetI, targetJ)){
                SearchCell neighbour = trackCells[targetI][targetJ];
                if(!closed.contains(neighbour) && !open.contains(neighbour)){
                    neighbour.parent = origin;
                    open.add(neighbour);
                }
            }
        }
    }

    /** inicializálja a trackCells-t megfelelő értékekkel */
    private void initTrackCells(List<Coin> coinList){
        for (int i = 0; i < track.length; i++) {
            for (int j = 0; j < track[0].length; j++) {
                trackCells[i][j] = new SearchCell(i, j);
                trackCells[i][j].totalCost = trackCells[i][j].heuristics;
            }
        }
        trackCells[state.i][state.j].reachCost = 0;

        updateCoinNeighbours(coinList);
    }

    /** frissíti a trackCells értékeit, hogy újabb keresést lehessen rajta végezni */
    private void resetTrackCells(Cell start,  List<Coin> coinList){
        for (int i = 0; i < track.length; i++) {
            for (int j = 0; j < track[0].length; j++) {
                trackCells[i][j].parent = null;
                trackCells[i][j].reachCost = Double.MAX_VALUE;
            }
        }
        trackCells[start.i][start.j].reachCost = 0;

        if(coinList.size() > 0) updateCoinNeighbours(coinList);
        else updateFinishNeighbours();
    }

    /** inicializálja az ágenst, meghatározza az ágens által lépett akciókat */
    private void init(){
        List<SearchCell> path = new ArrayList<>();

        initTrackCells(coinList);
        SearchCell start = trackCells[state.i][state.j];
        for(Coin coin: coins) {
            List<SearchCell> foundPath = aStar(start, true);
            path.addAll(foundPath);
            start = foundPath.remove(foundPath.size()-1);
            System.out.println(1);

            final Cell _curPos = new Cell(start.i, start.j);
            coinList.removeIf(c -> c.i == _curPos.i && c.j == _curPos.j);
            start.hasCoin = false;

            resetTrackCells(start, coinList);
        }
        System.out.println("affinito");

        resetTrackCells(start, new ArrayList<>());
        path.addAll(aStar(start, false));

        actions = new ArrayList<Direction>();
        for(int i = 1; i < path.size(); i++){
            if(path.get(i-1).i == path.get(i).i && path.get(i-1).j == path.get(i).j && path.get(i-1).velocity.i == path.get(i).velocity.i && path.get(i-1).velocity.j == path.get(i).velocity.j){
                continue;
            }
            actions.add(new Direction(path.get(i).velocity.i - path.get(i-1).velocity.i, path.get(i).velocity.j - path.get(i-1).velocity.j));
        }
    }

    /**
     * A fő metódus, amely megadja hogy egy adott körben (állapotban) mit lép az ágens
     * @param remainingTime Az ágens hátralévő ideje.
     * @return az elmozdulás iránya
     */
    @Override
    public Direction getDirection(long remainingTime) {
        return actionIndex < actions.size() ? actions.get(actionIndex++) : new Direction(0, 0);
    }
}
