<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="java.util.List" %>
<%@ page import="javax.jdo.PersistenceManager" %>
<%@ page import="javax.jdo.Query" %>
<%@ page import="fr.openbike.object.Network" %>
<%@ page import="fr.openbike.PMF" %>

<html>
  <body>
  <p>Current Networks : </p>
<%
	PersistenceManager pm = PMF.get().getPersistenceManager();
	Query query = pm.newQuery(Network.class);
    List<Network> networks = (List<Network>) query.execute();
    if (networks.isEmpty()) {
%>
<p>No networks !</p>
<%
	} else {
        for (Network n : networks) {
            
%>
<blockquote><%= n.getId() %> : <%= n.getCity() %></blockquote>
<%
        }
    }
    pm.close();
%>


Insert new Network
  <form action="/internal/insertnetwork" method="post">
    <div>ID : <input type="text" name="id" /></div>
    <div>Name : <input type="text" name="name" /></div>
    <div>City : <input type="text" name="city" value=""/></div>
    <div>Special Station Name : <input type="text" name="specialName" value=""/></div>
    <div>Longitude : <input type="text" name="longitude" value=""/></div>
    <div>Latitude : <input type="text" name="latitude" value=""/></div>
    <div>Server : <input type="text" name="server" value=""/></div>
    <div><input type="submit" value="Insert Network" /></div>
    
  </form>

  </body>
</html>