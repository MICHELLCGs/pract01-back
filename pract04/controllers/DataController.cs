using Microsoft.AspNetCore.Mvc;
using pract04.Models;
using System.IO;
using System.Text.Json;

namespace pract04.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class DataController : ControllerBase
    {
        private readonly string _jsonFilePath = Path.Combine(Directory.GetCurrentDirectory(), "Data", "recommendations.json");

        [HttpGet]
        public ActionResult<ApiResponse> Get()
        {
            if (!System.IO.File.Exists(_jsonFilePath))
            {
                return NotFound("JSON file not found.");
            }

            var jsonString = System.IO.File.ReadAllText(_jsonFilePath);

            // Deserializar el JSON
            var jsonOptions = new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            };

            try
            {
                var recommendationsDict = JsonSerializer.Deserialize<Dictionary<string, List<Person>>>(jsonString, jsonOptions);
                
                if (recommendationsDict != null && recommendationsDict.TryGetValue("recommendations", out var persons))
                {
                    var apiResponse = new ApiResponse
                    {
                        Persons = persons
                    };
                    return Ok(apiResponse);
                }

                return BadRequest("Error parsing JSON or no recommendations found.");
            }
            catch (JsonException ex)
            {
                return BadRequest($"JSON Error: {ex.Message}");
            }
        }
    }
}