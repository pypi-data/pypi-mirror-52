# csv2graph2web


## Install

### Install

    ```
    % pip install csv2graph2web
    ```
    
    or

    ```
    % pip install git+https://github.com/mastnk/csv2graph2web
    ```
    
    or

    ```
    % git clone https://github.com/mastnk/csv2graph2web
    % cd csv2grap2web
    % pip install .
    ```
    

### Uninstall

    ```
    % pip uninstall csv2graph2web
    ```

## Setup the webserver

### Direct setup via scp

   ```
   % cgw_copy --server yourhost.com --port 22 --login_name yourname --dir www/cgw
   ```
   
   - **server** specify your host server name.
   
   - **port** port for ssh (defulat: 22).
   
   - **login_name** specify your login name for the host server.
   
   - **dir** specify the directory which you want to install on the host sever.


### Get cgi file

   ```
   % cgw_copy
   % ls -l
   ```
   
   Then, you can find the cgi file *cgw.cgi* and the directory *graphs*.
   Please upload those two to your web server.


## Example code
    '''
    from csv2graph2web import csv2graph2web as cgw

    URL = '' # specify the URL for the cgw.cgi

    csv_filename = 'a.csv'    
    line = 'epoch, loss, acc, val_loss, val_acc'
    with open( csv_filename, 'w' ) as fout:
        fout.write( line + '\n' )

    graph_params = []
    opt = {'xlabel':'Epoch', 'legend':True}

    opt['title'] = 'acc'
    graph_params.append( ([('epoch', 'acc'), ('epoch', 'val_acc')], opt.copy()) )
    opt['title'] = 'loss'
    graph_params.append( ([('epoch', 'loss'), ('epoch', 'val_loss')], opt.copy()) )	

    for epoch in range(300):
        
        # some processes
        
        # dummy code
        loss = epoch
        acc = epoch / 300
        val_loss = loss * 0.9
        val_acc = acc * 0.9
        # dummy code
        
    
        if( epoch % 10 ):
            
            line = '{}, {}, {}, {}, {}'.format( epoch, loss, acc, val_loss, val_acc )
            with open( csv_filename, 'a' ) as fout:
                fout.write( line + '\n' )
            
            try:
                cgw.csv2graph2web( URL=URL, dir_name='tmp', csv_filename=csv_filename, graph_params=graph_params )
            except:
                pass
    '''
    
    Then, you can see the graphs in the *URL*.
    
## Scripts

### cgw_copy
	It generate the cgi for the web server.

    ```
    % cgw_copy -h
    ```

## Functions

### csv2graph2web( URL, dir_name, csv_filename, graph_params ) -> None

    - **URL**
        The url which represents the *cgw.cgi*. 
        You can also check the graphs from this URL.
    
    - **dir_name**
        The title of graphs. It appears in the html.

    - **csv_filename**

    - **graph_params**
        graph_params = [ list_params, opt ]
        
        - **list_params**
            list_params = [(x0,y0), (x1,y1), ...]
            
            xn: The index of x axis

            yn: The index of y axis
        
        - **opt**
        	dictionary of the options: *title*, *xlabel*, *ylabel*

