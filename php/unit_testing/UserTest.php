<?php


use PHPUnit\Framework\TestCase;

class StackTest extends TestCase 

{ 
	//Assert array as empty 
	public function testEmpty()
	{
		$stack = [];
		$this->asserEmpty($stack); 
		
		return $stack; 
		
	}
	
	//Test push and pop 
	public function testPushandPop()
	
	{
		$stack = [];
		$this->assertEquals(0,count($stack));
		
		array_push($stack, 'foo');
		$this->assertEquals('foo',$stack[count($stack)-1]);
		$this->assertEquals(1, count($stack));
		
		$this->assertEquals('foo', array_pop($stack));
		$this->assertEquals(0, count($stack));
		
	}
}


final class UserTest extends TestCase
{
    public function testCreateUser() {
		
		$user = user('student')->create();
		
        $this->assertTrue(true);
		

    }

}

?>