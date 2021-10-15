package shinylearner.helper;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.Set;

/** This class contains helper methods for dealing with Java collections and lists. Many of these implement functionality that circumvents some of the awkwardness and verbostity of dealing with lists in Java.
 * @author Stephen Piccolo
 */
public class ListUtilities
{
    /** Converts an array of String objects to a list of String objects.
     *
     * @param values Array of String objects
     * @return List of String objects
     */
    public static ArrayList<String> CreateStringList(String... values)
    {
        ArrayList<String> results = new ArrayList<String>();
        if (values.length > 0)
            Collections.addAll(results, values);
        return results;
    }

    /** Converts a generic collection of objects into a list of String objects.
     *
     * @param values Collection of objects
     * @return List of String objects
     */
    public static ArrayList<String> CreateStringList(Collection<String> values)
    {
        ArrayList<String> results = new ArrayList<String>();

        for (Object value : values)
            results.add(String.valueOf(value));

        return results;
    }

    /** Identifies all unique String values in a list.
     *
     * @param values List of String values
     * @return Unique values
     */
    public static ArrayList<String> GetUniqueValues(ArrayList<String> values)
    {
        return new ArrayList<String>(new LinkedHashSet<String>(values));
    }

    /** Identifies all values in a String list that start with a given String value.
     *
     * @param values List of values to be tested
     * @param pattern String value to be matched
     * @return List subset
     */
    public static ArrayList<String> GetValuesStartingWith(ArrayList<String> values, String pattern)
    {
        ArrayList<String> results = new ArrayList<String>();

        for (String value : values)
            if (value.startsWith(pattern))
                results.add(value);

        return results;
    }
    
    /** Identifies all values in a String list that do not start with a given String value.
    *
    * @param values List of values to be tested
    * @param pattern String value to be matched
    * @return List subset
    */
   public static ArrayList<String> GetValuesNotStartingWith(ArrayList<String> values, String pattern)
   {
       ArrayList<String> results = new ArrayList<String>();

       for (String value : values)
           if (!value.startsWith(pattern))
               results.add(value);

       return results;
   }

    /** Finds the intersection between two lists of String objects.
     *
     * @param list1 First list
     * @param list2 Second list
     * @return Intersection list (contains values that exist in both lists)
     */
    public static ArrayList<String> Intersect(ArrayList<String> list1, ArrayList<String> list2)
    {
        if (list1.size() == 0)
            return list2;

        Set<String> intersection = new HashSet<String>(list1);
        intersection.retainAll(new HashSet<String>(list2));
        return new ArrayList<String>(intersection);
    }
    
    public static HashSet<String> Intersect(Set<String> set1, Set<String> set2)
    {
        set1.retainAll(set2);
        return new HashSet<String>(set1);
    }

    /** For a list of String objects, this method identifies all objects that contain a given value and replaces that text with another value.
     *
     * @param list List of String objects
     * @param from Value to search for
     * @param to Value with which to replace matches
     * @return Replaced list of String objects
     */
    public static ArrayList<String> Replace(ArrayList<String> list, String from, String to)
    {
        ArrayList<String> newList = new ArrayList<String>();

        for (String x : list)
            newList.add(x.replace(from, to));

        return newList;
    }

    /** This method converts a list of String objects to a single String representation and inserts a delimiter between each object.
     * 
     * @param list List of String objects
     * @param delimiter Delimiter
     * @return Formatted String representation
     */
    public static String Join(ArrayList<String> list, String delimiter)
    {
        if (list.isEmpty())
            return "";

        StringBuilder sb = new StringBuilder();

        for (String x : list)
            sb.append(x + delimiter);

        sb.delete(sb.length() - delimiter.length(), sb.length());

        return sb.toString();
    }

    /** Convenience methods that makes it easier to sort a collection
     *
     * @param list Collection to sort
     * @return Sorted list
     */
    public static ArrayList<String> Sort(Collection<String> list)
    {
        ArrayList<String> newList = new ArrayList<String>(list);
        Collections.sort(newList);
        return newList;
    }

    /** Convenience methods that makes it easier to sort a String list
     *
     * @param list List to sort
     * @return Sorted list
     */
	public static ArrayList<String> SortStringList(ArrayList<String> list)
    {
    	return (ArrayList<String>)Sort(list);
    }

    /** This method creates a new list with each element of the input list in its lower-case representation.
     *
     * @param list List to be converted to lower case
     * @return New list converted to lower case
     */
    public static ArrayList<String> ToLowerCase(ArrayList<String> list)
    {
        ArrayList<String> newList = new ArrayList<String>();

        for (String x : list)
            newList.add(x.toLowerCase());

        return newList;
    }
}