<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>

<head>
    
    <meta http-equiv="Content-type" content="text/html; charset=utf-8">
    <title>ask Edsger</title>
    
    <style>
        * { margin: 0; padding: 0;}
        body { background: #555;}
        #calculator { width: 300px; border: 1px solid #333; margin: 80px auto;}
        #expression-arrow { background: black; font-size: 20px; color: green;}
        #expression { width: 280px; border: none; font-size: 20px; background: black; color: green;}
        #results { width: 300px; border: none; border-bottom: 1px solid black; font-size: 20px; background: black; color: green;}
        #submit { display: none; }
    </style>

  <script type="text/javascript" src="scripts/jquery-1.4.2.min.js"></script>

    
    <script>
        $(document).ready(function() {
            $("form").submit(function() {
                
                $.get("evaluate", $(this).serialize(), function(data){
                    // output the expression
                    $('#results').html(
                        $('#expression').val() + " = \n\t" + data + "\n\n" + $('#results').html()
                    );
                    // output the result
                    
                });
                
              return false;
            });
        });
    </script>
 
</head>
<body>
    <div id="calculator">
        <form action="">
            <p id="expression-arrow">><input type="text" name="expression" value="" id="expression"></p>
            <p><input type="submit" value="Continue &rarr;" id="submit"></p>
        </form>
        <textarea disabled="true" id="results" rows="20" >Type a mathematical expression above (e.g. 5+5), then press Enter</textarea>
    </div>
</body>
</html>

