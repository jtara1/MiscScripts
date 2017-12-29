Point 
World world = GameServer.INSTANCE.getGameUniverse().getWorld()
World world = getWorld();
int x = getX();


	
@Override	
public void setDead(boolean dead) {
	super().setDead(dead);
	spawnBiomassInPlace();	
}

private void spawnBiomassInPlace() {

	int x = getX();
	int y = getY();
	World world = getWorld();
	
	BiomassBlob biomassBlob = new BiomassBlob();
		biomassBlob.setObjectId(GameServer.INSTANCE.getGameUniverse().getNextObjectId());
		// biomassBlob.setStyle(0); //TODO: set style depending on difficulty level? or random? from config?
		biomassBlob.setBiomassCount(yield);
		biomassBlob.setX(x);
		biomassBlob.setY(y);
		biomassBlob.setWorld(world);	
}