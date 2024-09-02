using System;
using System.Collections.Generic;

namespace pract04.Models
{
    public class Person
    {
        public int PersonID { get; set; }
        public string Name { get; set; }
        public string First { get; set; }
        public string Last { get; set; }
        public string Middle { get; set; }
        public string Email { get; set; }
        public string Phone { get; set; }
        public string Fax { get; set; }
        public string Title { get; set; }
    }

    public class ApiResponse
    {
        public List<Person> Persons { get; set; }
    }
}
