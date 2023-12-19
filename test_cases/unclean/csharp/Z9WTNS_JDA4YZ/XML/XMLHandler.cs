using System.Xml.Serialization;

namespace Z9WTNS_JDA4YZ.Xml
{
    internal static class XmlHandler
    {
        internal static bool InitializeXmlData(string filePath)
        {
            try
            {
                string? directoryPath = Path.GetDirectoryName(filePath);

                if (directoryPath == null) return false;

                if (!Directory.Exists(directoryPath))
                {
                    Directory.CreateDirectory(directoryPath);
                }

                if (!File.Exists(filePath))
                {
                    File.Create(filePath).Dispose();
                }

                return true;
            }
            catch (IOException exception)
            {
                Console.WriteLine(exception.Message);

                return false;
            }
        }

        internal static List<T> ReadObjectsFromXml<T>(string filePath)
        {
            return ReadObjectsFromXmlAsync<T>(filePath).Result;
        }

        private static Task<List<T>> ReadObjectsFromXmlAsync<T>(string filePath)
        {
            XmlSerializer serializer = new XmlSerializer(typeof(List<T>));
            var objects = new List<T>();

            try
            {
                using (StreamReader reader = new StreamReader(filePath))
                {
                    var deserialized = reader.Peek() == -1 ? null : serializer.Deserialize(reader);

                    if (deserialized != null)
                        objects = (List<T>)deserialized;
                }
            }
            catch (IOException exception)
            {
                Console.WriteLine(exception.Message);
            }

            return Task.FromResult(objects);
        }

        internal static bool AppendObjectToXml<T>(string filePath, T appendedObject)
        {
            return AppendObjectToXmlAsync(filePath, appendedObject).Result;
        }

        private static async Task<bool> AppendObjectToXmlAsync<T>(string filePath, T appendedObject)
        {
            try
            {
                List<T> objects = ReadObjectsFromXml<T>(filePath);

                objects.Add(appendedObject);

                XmlSerializer serializer = new XmlSerializer(typeof(List<T>));

                using (var stream = new MemoryStream())
                {
                    using (var fileStream = new FileStream(filePath, FileMode.OpenOrCreate))
                    {
                        serializer.Serialize(stream, objects);
                        stream.Seek(0, SeekOrigin.Begin);
                        await stream.CopyToAsync(fileStream);

                        return true;
                    }
                }
            }
            catch (IOException exception)
            {
                Console.WriteLine(exception.Message);
                return false;
            }
        }
    }
}
