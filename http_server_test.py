import unittest
import os
import http_server


class RequestAndSplitTests(unittest.TestCase):

    def test_get_request(self):
        msg = 'GET /directory/file.html HTTP/1.1\r\ntextthat\r\ndoesntmatter'
        expected = 'GET /directory/file.html HTTP/1.1'
        result = http_server.get_request(msg)
        self.assertEqual(expected, result)

    def test_split_request(self):
        request = 'GET /directory/file.html HTTP/1.1'
        expected = ['GET', '/directory/file.html', 'HTTP/1.1']
        result = http_server.split_request(request)
        self.assertEqual(expected, result)

    def test_get_method(self):
        lst = ['GET', '/directory/file.html', 'HTTP/1.1']
        expected = 'GET'
        result = http_server.get_method(lst)
        self.assertEqual(expected, result)

    def test_get_uri(self):
        lst = ['GET', '/directory/file.html', 'HTTP/1.1']
        expected = '/directory/file.html'
        result = http_server.get_uri(lst)
        self.assertEqual(expected, result)


class MethodTests(unittest.TestCase):

    def setUp(self):
        self.get = ['GET', '/directory/file.html', 'HTTP/1.1']
        self.post = ['POST', '/directory/file.html', 'HTTP/1.1']
        self.put = ['PUT', '/directory/file.html', 'HTTP/1.1']
        self.delete = ['DELETE', '/directory/file.html', 'HTTP/1.1']
        self.other = ['not even a method', '/directory/file.html', 'HTTP/1.1']

    def test_get(self):
        self.assertTrue(http_server.check_method, self.get)

    def test_post(self):
        self.assertRaises(
            ValueError, http_server.check_method, self.post)

    def test_put(self):
        self.assertRaises(
            ValueError, http_server.check_method, self.put)

    def test_delete(self):
        self.assertRaises(
            ValueError, http_server.check_method, self.delete)

    def test_other(self):
        self.assertRaises(
            ValueError, http_server.check_method, self.other)


class URIAndMimetypeTests(unittest.TestCase):

    def setUp(self):
        self.rootpath = '/home/jordan/webroot'
        self.textfile = '/sample.txt'
        self.pngfile = '/images/sample_1.png'
        self.jpgfile = '/images/JPEG_example.jpg'
        self.folder = '/images/'
        self.missing = '/nonexistent.exe'

    def test_text_file(self):
        with open(self.rootpath + self.textfile, 'rb') as infile:
            f = infile.read()
        m = '\r\nContent-Type: text/plain'
        expected = (f, m)
        result = http_server.get_content(self.textfile)
        self.assertEqual(expected, result)

    def test_png_file(self):
        with open(self.rootpath + self.pngfile, 'rb') as infile:
            f = infile.read()
        m = '\r\nContent-Type: image/png'
        expected = (f, m)
        result = http_server.get_content(self.pngfile)
        self.assertEqual(expected, result)

    def test_jpg_file(self):
        with open(self.rootpath + self.jpgfile, 'rb') as infile:
            f = infile.read()
        m = '\r\nContent-Type: image/jpeg'
        expected = (f, m)
        result = http_server.get_content(self.jpgfile)
        self.assertEqual(expected, result)

    def test_dir(self):
        f = '\r\n'.join(os.listdir(self.rootpath + self.folder))
        m = '\r\nContent-Type: text/plain'
        expected = (f, m)
        result = http_server.get_content(self.folder)
        self.assertEqual(expected, result)

    def test_missing(self):
        self.assertRaises(ValueError, http_server.get_content, self.missing)


class ResponseTests(unittest.TestCase):

    def test_404(self):
        params = ('404 Not found', '', '404 Not found')
        expected = 'HTTP/1.1 404 Not found\r\n\r\n404 Not found'
        result = http_server.build_response(*params)
        self.assertEqual(expected, result)

    def test_405(self):
        params = ('405 Method not allowed', '', '405 Method not allowed')
        expected = ('HTTP/1.1 405 Method not allowed' +
                    '\r\n\r\n405 Method not allowed')
        result = http_server.build_response(*params)
        self.assertEqual(expected, result)

    def test_200_text(self):
        m, c = http_server.get_content('/sample.txt')
        params = ('200 OK', m, c)
        expected = 'HTTP/1.1 200 OK' + m + '\r\n\r\n' + c
        result = http_server.build_response(*params)
        self.assertEqual(expected, result)

    def test_200_image(self):
        m, c = http_server.get_content('/images/sample_1.png')
        params = ('200 OK', m, c)
        expected = 'HTTP/1.1 200 OK' + m + '\r\n\r\n' + c
        result = http_server.build_response(*params)
        self.assertEqual(expected, result)

    def test_200_folder(self):
        m, c = http_server.get_content('/images/')
        params = ('200 OK', m, c)
        expected = 'HTTP/1.1 200 OK' + m + '\r\n\r\n' + c
        result = http_server.build_response(*params)
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
